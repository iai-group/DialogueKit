"""Evaluation module"""
import warnings
import yaml
import numpy as np
from copy import deepcopy
from collections import defaultdict
from typing import List, Dict, Union, Optional, Any
from dialoguekit.core.dialogue import Dialogue, DialogueParticipant
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.models.satisfaction_classifier import (
    SatisfactionClassifierSVM,
)

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
    def __init__(self) -> None:
        self.dialogues = []
        self.dialogue_lengths = []

    def load_dialogue(
        self, dialogue_history: Union[List[Dialogue], Dialogue]
    ) -> None:
        if isinstance(dialogue_history, Dialogue):
            dialogue_history = [dialogue_history]

        self.dialogues = dialogue_history

    def success(
        self, interaction_model_path: str, dialogue_history: List[Dialogue]
    ):
        with open(interaction_model_path) as yaml_file:
            self.interaction_model = yaml.load(
                yaml_file, Loader=yaml.FullLoader
            )
        self.interaction_model["expected_responses"]
        successes = []
        for dialogue in dialogue_history:
            last_user_utterance = None
            dialogue_success = 0
            agent_utterance_count = (
                sum(
                    1
                    for utterance in dialogue.utterances
                    if utterance.get("sender") == DialogueParticipant.AGENT
                )
                - 1
            )
            for utterance in dialogue.utterances:
                if (
                    utterance.get("sender") == DialogueParticipant.AGENT
                    and last_user_utterance is not None
                ):
                    if utterance.get(
                        "utterance"
                    ).intent.label in self.interaction_model.get(
                        "expected_responses"
                    ).get(
                        last_user_utterance.intent.label, []
                    ):
                        dialogue_success += 1

                if utterance.get("sender") == DialogueParticipant.USER:
                    last_user_utterance = utterance.get("utterance")
            successes.append(dialogue_success / agent_utterance_count)

        return successes

    def avg_turns(
        self, dialogue_history: List[Dialogue], force_rebuild: bool = True
    ) -> float:
        """Calculates the AvgTurns for the dialogues

        Args:
            dialogue_history: list of completed Dialogues
        """

        if force_rebuild:
            for dialogue in dialogue_history:
                dialogue_turns = 0
                first_participant = None
                last_participant = None
                for dialogue_act in dialogue.utterances:
                    if first_participant is None:
                        first_participant = dialogue_act.get("sender")
                    if dialogue_act.get("sender") == first_participant:
                        last_participant = dialogue_act.get("sender")
                        continue
                    else:
                        if dialogue_act.get("sender") == last_participant:
                            continue
                        else:
                            dialogue_turns += 1

                self.dialogue_lengths.append(dialogue_turns)

        return (
            sum(self.dialogue_lengths) / len(self.dialogue_lengths),
            np.std(self.dialogue_lengths),
        )

    def user_act_ratio(
        self,
        dialogue_history: List[Dialogue],
    ) -> Dict[str, float]:

        statistics = defaultdict(float)
        for dialogue in dialogue_history:
            for utterance in dialogue.utterances:
                sender = utterance.get("sender").name
                statistics[sender] += 1

        if len(statistics.keys()) > 2:
            raise TypeError(
                f"There are more then 2 participants: {statistics.keys()}"
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
        dialogue_history: List[Dialogue],
        config: Optional[Dict[str, Union[int, float]]] = None,
    ) -> List[Union[int, float]]:

        warnings.warn("This function does not yet penalize 'Repeat' actions")

        if config is None:
            config = _REWARD_CONFIG

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

        # * Check if all necessary Intents are included.
        results = self._check_included_intents(
            results=results, config=config, dialogue_history=dialogue_history
        )

        # * Check for Repeats
        reward = config["full_set_points"]
        rewards = [reward for i in range(len(dialogue_history))]
        for i, dialogue in enumerate(dialogue_history):

            last_intent = None
            last_sender = None
            repeat_intents = 0

            # Start dialogue with Agent first.
            for j, utterance in enumerate(dialogue.utterances):
                if utterance.get("sender") == DialogueParticipant.AGENT:
                    dialogue_utterances_start_agent = dialogue.utterances[j:]
                    break
            for j, utterance in enumerate(dialogue_utterances_start_agent):
                if last_sender is None:
                    last_sender = utterance.get("sender")
                    last_intent = utterance.get("utterance").intent
                    continue
                if last_sender == utterance.get("sender"):
                    if last_intent == utterance.get("utterance").intent:
                        repeat_intents += 1
                        last_intent = None
                        last_sender = utterance.get("sender")
                        continue
                last_intent = utterance.get("utterance").intent
                last_sender = utterance.get("sender")

            results["dialogues"][i]["repeats"] = repeat_intents
            results["dialogues"][i]["reward"] -= repeat_intents
            rewards[i] -= repeat_intents

        # * Calculate USER/AGENT ratios.
        results = self._user_agent_ratio(
            results=results, config=config, dialogue_history=dialogue_history
        )

        for results_dialogue in results["dialogues"]:
            results_dialogue["reward"] = max(0, results_dialogue["reward"])

        return results

    def _user_agent_ratio(
        self,
        dialogue_history: List[Dict[str, Any]],
        config: Dict[str, Any],
        results: Dict[str, Any],
    ) -> Dict[str, Any]:
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
        dialogue_history: List[Dict[str, Any]],
        config: Dict[str, Any],
        results: Dict[str, Any],
    ) -> Dict[str, Any]:
        reward = config["full_set_points"]
        dialogue_intents = [
            Intent(ut.get("utterance").intent.label.split(".")[0])
            for dialogue in dialogue_history
            for ut in dialogue.utterances
        ]
        dialogue_intents.extend(
            [
                Intent(ut.get("utterance").intent.label)
                for dialogue in dialogue_history
                for ut in dialogue.utterances
            ]
        )
        dialogue_intents_set = set(dialogue_intents)

        for intent, penalty in config.get("intents").items():
            if Intent(intent) not in dialogue_intents_set:
                reward -= penalty
                results["missing_intents"].append(intent)

        for results_dialogue in results["dialogues"]:
            results_dialogue["reward"] = reward

        return results

    def satisfaction(self, dialogue_history: List[Dialogue]):
        satisfactions = []
        sc = SatisfactionClassifierSVM()
        for dialogue in dialogue_history:
            satisfactions.append(sc.classify_last_n_dialogue(dialogue=dialogue))

        return satisfactions
