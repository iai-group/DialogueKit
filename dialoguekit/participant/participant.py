"""Interface defining core Participant functionality."""
from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from dialoguekit.core.annotated_utterance import AnnotatedUtterance
    from dialoguekit.manager.dialogue_manager import DialogueManager


class DialogueParticipant(Enum):
    """Represents possible dialogue participants."""

    AGENT = 0
    USER = 1


class Participant(ABC):
    def __init__(self, id: str, type: DialogueParticipant) -> None:
        """Represents a Participant.

        Both Agents and Users are Participants.

        Args:
            agent_id: Agent ID.
            agent_type: Agent type (default: BOT).
        """
        self._id = id
        self._type = type
        self._dialogue_manager = None

    @property
    def id(self):
        return self._id

    def to_dict(self) -> Dict[str, str]:
        return {"id": str(self._id), "type": str(self._type.name)}

    def connect_dialogue_manager(
        self, dialogue_manager: DialogueManager
    ) -> None:
        """Connects the Dialogue Manager instance for the Participant.

        Args:
            dialogue_manager: A DialogueManager instance.
        """
        self._dialogue_manager = dialogue_manager

    def receive_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Responds to the user with an AnnotatedUtterance.

        Args:
            utterance: The other Participant's Utterance.
        """
        pass
