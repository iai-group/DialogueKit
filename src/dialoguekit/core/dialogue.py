"""Interface representing the sequence of utterances in a dialogue."""

from datetime import datetime
from enum import Enum
from typing import Dict, List

from dialoguekit.core.utterance import Utterance


class DialogueParticipant(Enum):
    """Represents possible dialogue participants."""

    AGENT = 0
    USER = 1


class Dialogue:
    """Represents a dialogue."""

    def __init__(self, agent_id: str, user_id: str) -> None:
        """Initializes the dialogue history.

        Args:
            agent_id: Agent ID.
            user_id: User ID.
        """
        self.__agent_id = agent_id
        self.__user_id = user_id
        self.__utterances = []

    @property
    def agent_id(self) -> str:
        return self.__agent_id

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def utterances(self) -> List[Dict]:
        return self.__utterances

    def __add_utterance(
        self, sender: DialogueParticipant, utterance: Utterance
    ) -> None:
        """Adds an utterance to the history.

        Args:
            sender: Sender of the utterance (AGENT or USER).
            utterance: An instance of Utterance.
        """
        self.__utterances.append(
            {
                "sender": sender,
                "timestamp": datetime.now(),
                "utterance": utterance,
            }
        )

    def add_agent_utterance(self, utterance: Utterance) -> None:
        """Adds an agent utterance.

        Args:
            utterance: An instance of utterance.
        """
        self.__add_utterance(DialogueParticipant.AGENT, utterance)

    def add_user_utterance(self, utterance: Utterance) -> None:
        """Adds a user utterance.

        Args:
            utterance: An instance of utterance.
        """
        self.__add_utterance(DialogueParticipant.USER, utterance)
