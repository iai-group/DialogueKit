"""Interface defining core Participant functionality."""

from __future__ import annotations
from abc import ABC
import enum
from typing import TYPE_CHECKING

from dialoguekit.core.utterance import Utterance

if TYPE_CHECKING:
    from dialoguekit.manager.dialogue_manager import DialogueManager


class Participant(ABC):
    """Represents a Participant.

    Both Agents and Users are Participants.
    """

    def __init__(self, id: str, type: enum) -> None:
        """Initializes the agent.

        Args:
            agent_id: Agent ID.
            agent_type: Agent type (default: BOT).
        """
        self.__id = id
        self._type = type
        self._dialogue_manager = None

    @property
    def id(self):
        return self.__id

    def connect_dialogue_manager(
        self, dialogue_manager: DialogueManager
    ) -> None:
        """Connects the Dialogue Manager instance for the Participant.

        Args:
            dialogue_manager: A DialogueManager instance.
        """
        self._dialogue_manager = dialogue_manager

    def receive_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new utterance.

        Args:
            utterance: The other Participant's Utterance.
        """
        pass
