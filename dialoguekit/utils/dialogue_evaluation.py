"""Evaluation module"""

import warnings
from collections import defaultdict
from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from dialoguekit.core.dialogue import Dialogue, DialogueParticipant
from dialoguekit.core.intent import Intent

# from dialoguekit.nlu.models.satisfaction_classifier import (
#     SatisfactionClassifier,
# )

# REWARD CONFIG PARAMETERS
# Initial points before deduction.
_CONFIG_FULL_SET_POINTS = "full_set_points"

# Intents that deduct points from _CONFIG_FULL_SET_POINTS if not present in the
# Dialogue.
_CONFIG_INTENTS = "intents"

# Deducted points for each time the agent repeats itself, in a row. Currently
# not used.
_REPEAT_PENALTY = "repeat_penalty"

# Deducted points for each turn.
_COST = "cost"


class Evaluator:
    """Dialogue evaluator.

    Evaluates a set of dialogues using standard metrics, see docs/Evaluation.md.

    Attributes:
        dialogues: A list of Dialogue objects to be evaluated.
        reward_config: A dictionary with reward settings. Example config can be
        seen in docs/Evaluation.md.
    """
    def __init__(
        self,
        dialogues: List[Dialogue],
        reward_config: Dict[str, Union[int, Dict[str, int]]],
    ) -> None:
        self.dialogues = dialogues
        self.dialogue_lengths = []
        self.reward_config = reward_config
        assert isinstance(self.dialogues, list)
        assert all(isinstance(dialogue, Dialogue) for dialogue in dialogues)
        assert "full_set_points" in self.reward_config
        assert "intents" in self.reward_config
        assert "repeat_penalty" in self.reward_config
        assert "cost" in self.reward_config

    def avg_turns(self) -> float:
        """Calculates the AvgTurns for the dialogues.

        AvgTurns reflects the average number of system-user turn pairs in a list
        of dialogues.
        """
        for dialogue in self.dialogues:
            dialogue_turns = 0
            for i in range(len(dialogue.utterances)):
                if (
                    i == 0
                    or dialogue.utterances[i - 1].get("sender")
                    == dialogue.utterances[i].get("sender")
                ):
                    continue
                else:
                    dialogue_turns += 1
            self.dialogue_lengths.append(dialogue_turns / 2)

        return sum(self.dialogue_lengths) / len(self.dialogue_lengths)

    def user_act_ratio(self) -> Dict[str, float]:
        """Computes the UserActRatio for the dialogues.

        UserActRatio per dialogue is computed as the ratio of user actions
        observed in the dialogue.
        """

        statistics = defaultdict(float)

        for dialogue in self.dialogues:
            for utterance in dialogue.utterances:
                sender = utterance.get("sender").name
                statistics[sender] += 1

        if len(statistics.keys()) > 2:
            raise TypeError(
                f"There are more than 2 participants: {statistics.keys()}"
            )
        statistics_copy = deepcopy(statistics)
        for sender in statistics.keys():
            for other_sender in statistics.keys():
                if sender == other_sender:
                    continue
                statistics_copy[f"{sender}/{other_sender}"] = statistics.get(
                    sender
                ) / statistics.get(other_sender)

        return statistics_copy

    def reward(
        self,
        dialogue_history: Optional[List[Dialogue]],
    ) -> List[Union[int, float]]:
        """Computes reward for the dialogues.

        Args:
            dialogue_history: list of completed Dialogue.
            config: dictionary with reward mappings, e.g., _REWARD_CONFIG.
        """
        warnings.warn("This function does not yet penalize 'Repeat' actions")
        if dialogue_history is None:
            dialogue_history = self.dialogues

        # Initialize result by checking which intents are included
        results = self._check_included_intents(
            dialogue_history=dialogue_history
        )

        # * Check for Repeats
        for i, dialogue in enumerate(dialogue_history):

            previous_intent = None
            previous_sender = None
            n_repeat_intents = 0

            # Start dialogue with Agent first.
            for j, utterance in enumerate(dialogue.utterances):
                if utterance.get("sender") == DialogueParticipant.AGENT:
                    dialogue_utterances_start_agent = dialogue.utterances[j:]
                    break
            previous_sender = dialogue_utterances_start_agent[0].get("sender")
            previous_intent = (
                dialogue_utterances_start_agent[0].get("utterance").intent
            )
            for j, utterance in enumerate(
                dialogue_utterances_start_agent, start=1
            ):
                if (
                    utterance.get("sender") == previous_sender
                    and previous_intent == utterance.get("utterance").intent
                ):
                    n_repeat_intents += 1
                    previous_intent = None
                    continue
                previous_intent = utterance.get("utterance").intent
                previous_sender = utterance.get("sender")

            results["dialogues"][i]["repeats"] = n_repeat_intents
            results["dialogues"][i]["reward"] -= n_repeat_intents

        # * Calculate USER/AGENT ratios.
        results = self._user_agent_ratio(
            results=results, dialogue_history=dialogue_history
        )

        for results_dialogue in results["dialogues"]:
            results_dialogue["reward"] = max(0, results_dialogue["reward"])

        return results

    def _user_agent_ratio(
        self,
        dialogue_history: Optional[List[Dialogue]],
        results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Computes number of user turns and reward across a list of dialogues.

        Args:
            dialogue_history: list of completed Dialogue.
            config: dictionary with reward mappings, e.g., _REWARD_CONFIG.
            results: dictionary to hold measured metrics.
        """
        if dialogue_history is None:
            dialogue_history = self.dialogues

        for i, dialogue in enumerate(dialogue_history):
            num_user_acts = sum(
                1
                for utterance in dialogue.utterances
                if utterance["sender"] == DialogueParticipant.USER
            )
            results["dialogues"][i]["user_turns"] = num_user_acts
            results["dialogues"][i][
                "reward"
            ] -= num_user_acts * self.reward_config.get("cost")
        return results

    def _check_included_intents(
        self, dialogue_history: List[Dialogue]
    ) -> Dict[str, Any]:
        """Sets initial reward for dialogues by checking which intents are
        supported.

        Args:
            dialogue_history: list of completed Dialogue.
            config: dictionary with reward mappings, e.g., _REWARD_CONFIG.
            results: dictionary to hold measured metrics.
        """
        if dialogue_history is None:
            dialogue_history = self.dialogues

        results = {
            "missing_intents": [],
            "dialogues": [
                {
                    "reward": self.reward_config["full_set_points"],
                    "user_turns": 0,
                    "repeats": 0,
                }
                for i in range(len(dialogue_history))
            ],
        }

        dialogue_intents = []
        reward = self.reward_config["full_set_points"]
        for dialogue in dialogue_history:
            for utterance in dialogue.utterances:
                if utterance["sender"] == DialogueParticipant.USER:
                    dialogue_intents.append(
                        Intent(utterance.get("utterance").intent.label.split(
                            "."
                        )[0])
                    )
                    dialogue_intents.append(utterance.get("utterance").intent)

        dialogue_intents_set = set(dialogue_intents)

        for intent_str, penalty in self.reward_config.get("intents").items():
            if Intent(intent_str) not in dialogue_intents_set:
                reward -= penalty
                results["missing_intents"].append(Intent(intent_str))

        for results_dialogue in results["dialogues"]:
            results_dialogue["reward"] = reward

        return results

    # def satisfaction(self, dialogue_history: List[Dialogue]) -> List[int]:
    #     """Classifies dialogue-level satisfaction score.

    #     Args:
    #         dialogue_history: list of completed Dialogue.
    #     """

    #     satisfactions = []

    #     if dialogue_history is None:
    #         dialogue_history = self.dialogues

    #     sc = SatisfactionClassifier()
    #     for dialogue in dialogue_history:
    #         satisfactions.append(sc.classify_last_n_dialogue(dialogue=dialogue))

    #     return satisfactions
