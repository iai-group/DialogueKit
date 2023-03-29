"""Abstract representation of core user-related data and functionality.

For communicating with an agent, the specific user instance needs to be
connected with a DialogueConnector by invoking
`register_dialogue_connector()`.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.participant import DialogueParticipant, Participant

if TYPE_CHECKING:
    from dialoguekit.connector.dialogue_connector import DialogueConnector


class UserType(Enum):
    """Represents different types of users (humans vs simulated users)."""

    HUMAN = 0
    SIMULATOR = 1


class User(Participant):
    def __init__(self, id: str, user_type: UserType = UserType.HUMAN) -> None:
        """Represents a user.

        Args:
            id: User ID.
            user_type: User type (default: HUMAN).
        """
        super().__init__(id=id, type=DialogueParticipant.USER)
        self._user_type = user_type

    def connect_dialogue_connector(self, dialogue_connector: DialogueConnector):
        """Connects the User with a DialogueConnector.

        Args:
            dialogue_connector: DialogueConnector instance.
        """
        super().connect_dialogue_connector(dialogue_connector)
        platform = self._dialogue_connector.get_platform()
        platform.register_user_callback(self.on_user_input)

    def on_user_input(self, text: str) -> None:
        """Gets called every time there is a new user input.

        Args:
            text: User input.
        """
        utterance = AnnotatedUtterance(
            text,
            participant=DialogueParticipant.USER,
        )
        self._dialogue_connector.register_user_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        platform = self._dialogue_connector.get_platform()
        platform.listen_for_user_input()
