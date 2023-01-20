"""Evaluation module."""

import warnings
from collections import defaultdict
from copy import deepcopy
from typing import Any, Dict, List, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.dialogue import Dialogue
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.models.satisfaction_classifier import (
    SatisfactionClassifierSVM,
)
from dialoguekit.participant.participant import DialogueParticipant

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
    def __init__(
        self, dialogues: List[Dialogue], reward_config: Dict[str, Any]
    ) -> None:
        """Dialogue evaluator.

        Evaluates a set of dialogues using standard metrics.

        Args:
            dialogues: A list of Dialogue objects to be evaluated.
            reward_config: A dictionary with reward settings. For an example
              config, consult the documentation.
        """
        self._dialogues = dialogues
        self._dialogue_lengths: List[Union[int, float]] = []
        self._reward_config = reward_config
        assert isinstance(self._dialogues, list)
        assert all(isinstance(dialogue, Dialogue) for dialogue in dialogues)
        assert _CONFIG_FULL_SET_POINTS in self._reward_config
        assert _CONFIG_INTENTS in self._reward_config
        assert _REPEAT_PENALTY in self._reward_config
        assert _COST in self._reward_config

    def avg_turns(self) -> float:
        """Calculates the AvgTurns for the dialogues.

        AvgTurns reflects the average number of system-user turn pairs in a list
        of dialogues.

        Returns:
            The computed metric as a float value.
        """
        for dialogue in self._dialogues:
            dialogue_turns = 0
            for i in range(len(dialogue.utterances)):
                if (
                    i == 0
                    or dialogue.utterances[i - 1].participant
                    == dialogue.utterances[i].participant
                ):
                    continue
                else:
                    dialogue_turns += 1
            self._dialogue_lengths.append(dialogue_turns / 2)

        return sum(self._dialogue_lengths) / len(self._dialogue_lengths)

    def user_act_ratio(self) -> Dict[str, float]:
        """Computes the UserActRatio for the dialogues.

        UserActRatio per dialogue is computed as the ratio of user actions
        observed in the dialogue.

        Returns:
            A dictionary with participant and ActRatio as key-value pairs.
        """
        statistics: Dict[str, float] = defaultdict(float)

        for dialogue in self._dialogues:
            for utterance in dialogue.utterances:
                sender = str(utterance.participant)
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

    def reward(self) -> Dict[str, List[Dict[str, float]]]:
        """Computes reward for the dialogues, according to the reward config.

        Reward is used to penalize agents that do not support a set of intents
        defined in the config file, and long dialogues.

        Returns:
            A dictionary with following structure (most important is "reward"):

            .. code:: python

                {
                    "missing_intents": [],
                    "dialogues": [{
                        "reward": int,
                        "user_turns": int,
                        "repeats": int,
                    }]
                }
        """
        warnings.warn("This function does not yet penalize 'Repeat' actions")

        # Initialize result by checking which intents are included
        results = self._check_included_intents()

        # Check for Repeats
        for i, dialogue in enumerate(self._dialogues):

            previous_intent = None
            previous_sender = None
            n_repeat_intents = 0

            # Start dialogue with Agent first.
            for j, utterance in enumerate(dialogue.utterances):
                if utterance.participant == DialogueParticipant.AGENT.name:
                    dialogue_utterances_start_agent = [
                        AnnotatedUtterance.from_utterance(u)
                        for u in dialogue.utterances[j:]
                    ]
                    break
            previous_sender = dialogue_utterances_start_agent[0].participant
            previous_intent = dialogue_utterances_start_agent[0].intent
            for j, annotated_utterance in enumerate(
                dialogue_utterances_start_agent, start=1
            ):
                if (
                    annotated_utterance.participant == previous_sender
                    and previous_intent == annotated_utterance.intent
                ):
                    n_repeat_intents += 1
                    previous_intent = None
                    continue
                previous_intent = annotated_utterance.intent
                previous_sender = annotated_utterance.participant

            results["dialogues"][i]["repeats"] = n_repeat_intents
            results["dialogues"][i]["reward"] -= n_repeat_intents

        # * Calculate USER/AGENT ratios.
        results = self._user_agent_ratio(results=results)

        for results_dialogue in results["dialogues"]:
            results_dialogue["reward"] = max(0, results_dialogue["reward"])

        return results

    def _check_included_intents(self) -> Dict[str, Any]:
        """Sets initial reward.

        Uses dialogues by checking which intents are supported.

        Returns:
            A dictionary to hold measured metrics relevant to reward.
        """
        results: Dict[str, List[Any]] = {
            "missing_intents": [],
            "dialogues": [
                {
                    "reward": self._reward_config["full_set_points"],
                    "user_turns": 0,
                    "repeats": 0,
                }
                for _ in range(len(self._dialogues))
            ],
        }

        dialogue_intents = []
        reward = self._reward_config["full_set_points"]
        for dialogue in self._dialogues:
            for utterance in dialogue.utterances:
                if (
                    isinstance(utterance, AnnotatedUtterance)
                    and utterance.participant == DialogueParticipant.USER.name
                ):
                    dialogue_intents.append(
                        Intent(utterance.intent.label.split(".")[0])
                    )
                    dialogue_intents.append(utterance.intent)

        dialogue_intents_set = set(dialogue_intents)

        for intent_str, penalty in self._reward_config.get("intents").items():
            if Intent(intent_str) not in dialogue_intents_set:
                reward -= penalty
                results["missing_intents"].append(Intent(intent_str))

        for results_dialogue in results["dialogues"]:
            results_dialogue["reward"] = reward

        return results

    def _user_agent_ratio(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Computes number of user turns and reward across a list of dialogues.

        Args:
            results: A dictionary to hold measured metrics that are relevant to
              compute the reward.

        Returns:
            Returns results, a dictionary to hold measured metrics. See reward
            function for structure of this dictionary.
        """
        for i, dialogue in enumerate(self._dialogues):
            num_user_acts = sum(
                1
                for utterance in dialogue.utterances
                if utterance.participant == DialogueParticipant.USER.name
            )
            results["dialogues"][i]["user_turns"] = num_user_acts
            results["dialogues"][i][
                "reward"
            ] -= num_user_acts * self._reward_config.get("cost")
        return results

    def satisfaction(
        self, satisfaction_classifier: SatisfactionClassifierSVM
    ) -> List[int]:
        """Classifies dialogue-level satisfaction score.

        Satisfaction is scored using a SatisfactionClassifier model. Based on
        last n turns, it computes a satisfaction score.

        Returns:
            A list with satisfaction score for each dialogue.
        """
        satisfactions = []

        for dialogue in self._dialogues:
            satisfactions.append(
                satisfaction_classifier.classify_last_n_dialogue(
                    dialogue=dialogue
                )
            )

        return satisfactions
