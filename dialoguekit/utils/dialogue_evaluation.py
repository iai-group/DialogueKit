"""Evaluation module"""
import warnings
from copy import deepcopy
from collections import defaultdict
from typing import List, Dict, Union, Optional
from dialoguekit.core.dialogue import Dialogue, DialogueParticipant
from dialoguekit.core.intent import Intent

_REWARD_CONFIG = {
    "full_set_points": 20,
    "intents": {
        "DISCLOSE": 4,
        "REFINEMENT": 4,
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

        return sum(self.dialogue_lengths) / len(self.dialogue_lengths)

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
        reward = config["full_set_points"]

        dialogue_intents = [
            Intent(ut.get("utterance").intent.label.split(".")[0])
            for dialogue in dialogue_history
            for ut in dialogue.utterances
        ]
        dialogue_intents_set = set(dialogue_intents)

        for intent, penalty in config.get("intents").items():
            if Intent(intent) not in dialogue_intents_set:
                reward -= penalty

        # TODO penalize "Repeat" actions
        rewards = [reward for i in range(len(dialogue_history))]

        for i, dialogue in enumerate(dialogue_history):
            num_user_acts = sum(
                1
                for utterance in dialogue.utterances
                if utterance["sender"] == DialogueParticipant.USER
            )
            rewards[i] -= num_user_acts * config.get("cost")

        rewards = [max(0, reward) for reward in rewards]
        return rewards
