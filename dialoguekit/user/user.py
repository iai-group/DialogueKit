"""Abstract representation of core user-related data and functionality.

For communicating with an agent, the specific user instance needs to be
connected with a DialogueManager by invoking `register_dialogue_manager()`.
"""

from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from dialoguekit.core.utterance import Utterance

if TYPE_CHECKING:
    from dialoguekit.manager.dialogue_manager import DialogueManager


class UserType(Enum):
    """Represents different types of users (humans vs. simulated users)."""

    HUMAN = 0
    SIMULATOR = 1


class User:
    """Represents a user."""

    def __init__(
        self, user_id: str, user_type: UserType = UserType.HUMAN
    ) -> None:
        """Initializes the user.

        Args:
            user_id: User ID.
            user_type: User type (default: HUMAN).
        """
        self.__user_id = user_id
        self._user_type = user_type
        self._dialogue_manager = None

    @property
    def user_id(self):
        return self.__user_id

    def connect_dialogue_manager(
        self, dialogue_manager: DialogueManager
    ) -> None:
        """Connects the Dialogue Manager instance for the user.

        Args:
            dialogue_manager: A DialogueManager instance.
        """
        self._dialogue_manager = dialogue_manager

    def receive_agent_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        # TODO: Move input part to Platform.
        text = input("Your response: ")
        response = Utterance(text)
        self._dialogue_manager.register_user_utterance(response)
