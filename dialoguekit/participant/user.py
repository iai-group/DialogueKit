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
    from dialoguekit.platforms.platform import Platform


class UserType(Enum):
    """Represents different types of users (humans vs simulated users)."""

    HUMAN = 0
    SIMULATOR = 1


class User(Participant):
    def __init__(
        self,
        id: str,
        user_type: UserType = UserType.HUMAN,
        platform: Platform = None,
    ) -> None:
        """Represents a user.

        Args:
            id: User ID.
            user_type: User type (default: HUMAN).
            platform: Platform instance (default: None).
        """
        super().__init__(id=id, type=DialogueParticipant.USER)
        self._user_type = user_type
        self._platform = platform

    def on_user_input(self, text: str) -> None:
        """Gets called every time there is a new user input.

        Args:
            text: User input.
        """
        utterance = AnnotatedUtterance(
            text, participant=DialogueParticipant.USER
        )
        self._dialogue_connector.register_user_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        self._platform.listen_for_user_input(self.on_user_input)
