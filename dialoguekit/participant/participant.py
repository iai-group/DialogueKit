"""Interface defining core Participant functionality."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from dialoguekit.connector.dialogue_connector import DialogueConnector
    from dialoguekit.core.annotated_utterance import AnnotatedUtterance


class DialogueParticipant(Enum):
    """Represents possible dialogue participants."""

    AGENT = 0
    USER = 1


class Participant(ABC):
    def __init__(self, id: str, type: DialogueParticipant) -> None:
        """Represents a Participant.

        Both Agents and Users are Participants.

        Args:
            id: Agent ID.
            type: Agent type (default: BOT).
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
        """Connects the Dialogue Connector instance for the Participant.

        Args:
            dialogue_connector: A DialogueConnector instance.
        """
        self._dialogue_connector = dialogue_connector

    @abstractmethod
    def receive_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Responds to the other participant with an AnnotatedUtterance.

        Args:
            annotated_utterance: The other Participant's Utterance.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError
