"""Interface defining core participant functionality."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from dialoguekit.connector.dialogue_connector import DialogueConnector
    from dialoguekit.core.utterance import Utterance


class DialogueParticipant(Enum):
    """Represents possible dialogue participants."""

    AGENT = 0
    USER = 1


class Participant(ABC):
    def __init__(self, id: str, type: DialogueParticipant) -> None:
        """Represents a participant.

        Both agents and users are participants.

        Args:
            id: Participant's ID.
            type: Participant's type.
        """
        self._id = id
        self._type = type
        self._dialogue_connector: DialogueConnector = None

    @property
    def id(self):
        """Returns the participant id."""
        return self._id

    def to_dict(self) -> Dict[str, str]:
        """Returns participant as a dictionary.

        Returns:
            A dictionary representation of the participant.
        """
        return {"id": str(self._id), "type": str(self._type.name)}

    def connect_dialogue_connector(
        self, dialogue_connector: DialogueConnector
    ) -> None:
        """Connects the DialogueConnector instance for the participant.

        Args:
            dialogue_connector: A DialogueConnector instance.
        """
        self._dialogue_connector = dialogue_connector

    @abstractmethod
    def receive_utterance(self, utterance: Utterance) -> None:
        """Responds to the other participant with an utterance.

        Args:
            utterance: The other participant's utterance.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError
