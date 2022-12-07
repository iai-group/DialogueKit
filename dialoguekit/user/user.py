"""Abstract representation of core user-related data and functionality.

For communicating with an agent, the specific user instance needs to be
connected with a DialogueConnector by invoking
`register_dialogue_connector()`.
"""

from __future__ import annotations

from enum import Enum

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.participant import DialogueParticipant, Participant


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

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        # TODO: Move input part to Platform.
        text = input("Your response: ")
        response = AnnotatedUtterance(
            text, participant=DialogueParticipant.USER
        )
        self._dialogue_connector.register_user_utterance(response)
