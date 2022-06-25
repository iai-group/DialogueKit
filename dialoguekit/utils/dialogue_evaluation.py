"""Evaluation module"""
import warnings
from copy import deepcopy
from collections import defaultdict
from typing import List, Dict, Union, Optional, Any
from dialoguekit.core.dialogue import Dialogue, DialogueParticipant
from dialoguekit.core.intent import Intent

# from dialoguekit.nlu.models.satisfaction_classifier import (
#     SatisfactionClassifier,
# )

_REWARD_CONFIG = {
    "full_set_points": 20,
    "intents": {
        "DISCLOSE": 4,
        "REVEAL.REFINE": 4,
        "INQUIRE": 4,
        "NAVIGATE": 4,
    },
    "repeat_penalty": 1,
    "cost": 1,
}


class Evaluator:
    def __init__(
        self, dialogue_history: Union[List[Dialogue], Dialogue]
    ) -> None:
        if isinstance(dialogue_history, Dialogue):
            dialogue_history = [dialogue_history]
        self.dialogues = dialogue_history
        self.dialogue_lengths = []

    def avg_turns(self, dialogue_history: Optional[List[Dialogue]]) -> float:
        """Calculates the AvgTurns for the dialogues

        Args:
            dialogue_history: list of completed Dialogue.
        """
        if dialogue_history is None:
            dialogue_history = self.dialogues

        for dialogue in dialogue_history:
            dialogue_turns = 0
            first_participant = dialogue.utterances[0].get("sender")
            previous_participant = None
            for dialogue_act in dialogue.utterances:
                if (
                    dialogue_act.get("sender") == first_participant
                    or dialogue_act.get("sender") == previous_participant
                ):
                    previous_participant = dialogue_act.get("sender")
                    continue
                else:
                    dialogue_turns += 1
            self.dialogue_lengths.append(dialogue_turns)

        return sum(self.dialogue_lengths) / len(self.dialogue_lengths)

    def user_act_ratio(
        self,
        dialogue_history: Optional[List[Dialogue]],
    ) -> Dict[str, float]:
        """Computes the UserActRatio for the dialogues.

        Args:
            dialogue_history: list of completed Dialogue.
        """

        statistics = defaultdict(float)

        if dialogue_history is None:
            dialogue_history = self.dialogues

        for dialogue in dialogue_history:
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
        config: Optional[Dict[str, Union[int, float]]] = None,
    ) -> List[Union[int, float]]:
        """Computes reward for the dialogues.

        Args:
            dialogue_history: list of completed Dialogue.
            config: dictionary with reward mappings, e.g., _REWARD_CONFIG.
        """
        warnings.warn("This function does not yet penalize 'Repeat' actions")

        if config is None:
            config = _REWARD_CONFIG

        if dialogue_history is None:
            dialogue_history = self.dialogues

        # Initialize result by checking which intents are included
        results = self._check_included_intents(
            config=config, dialogue_history=dialogue_history
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
            results=results, config=config, dialogue_history=dialogue_history
        )

        for results_dialogue in results["dialogues"]:
            results_dialogue["reward"] = max(0, results_dialogue["reward"])

        return results

    def _user_agent_ratio(
        self,
        dialogue_history: Optional[List[Dialogue]],
        config: Optional[Dict[str, Any]],
        results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Computes number of user turns and reward across a list of dialogues.

        Args:
            dialogue_history: list of completed Dialogue.
            config: dictionary with reward mappings, e.g., _REWARD_CONFIG.
            results: dictionary to hold measured metrics.
        """

        if config is None:
            config = _REWARD_CONFIG

        if dialogue_history is None:
            dialogue_history = self.dialogues

        for i, dialogue in enumerate(dialogue_history):
            num_user_acts = sum(
                1
                for utterance in dialogue.utterances
                if utterance["sender"] == DialogueParticipant.USER
            )
            results["dialogues"][i]["user_turns"] = num_user_acts
            results["dialogues"][i]["reward"] -= num_user_acts * config.get(
                "cost"
            )
        return results

    def _check_included_intents(
        self,
        dialogue_history: List[Dialogue],
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Sets initial reward for dialogues by checking which intents are
        supported.

        Args:
            dialogue_history: list of completed Dialogue.
            config: dictionary with reward mappings, e.g., _REWARD_CONFIG.
            results: dictionary to hold measured metrics.
        """

        if config is None:
            config = _REWARD_CONFIG

        if dialogue_history is None:
            dialogue_history = self.dialogues

        results = {
            "missing_intents": [],
            "dialogues": [
                {
                    "reward": config["full_set_points"],
                    "user_turns": 0,
                    "repeats": 0,
                }
                for i in range(len(dialogue_history))
            ],
        }

        dialogue_intents = []
        reward = config["full_set_points"]
        for dialogue in dialogue_history:
            for ut in dialogue.utterances:
                if ut["sender"] == DialogueParticipant.USER:
                    dialogue_intents.append(
                        Intent(ut.get("utterance").intent.label.split(".")[0])
                    )
                    dialogue_intents.append(ut.get("utterance").intent)

        dialogue_intents_set = set(dialogue_intents)

        for intent_str, penalty in config.get("intents").items():
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
