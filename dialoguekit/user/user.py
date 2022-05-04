"""Abstract representation of core user-related data and functionality.

For communicating with an agent, the specific user instance needs to be
connected with a DialogueManager by invoking `register_dialogue_manager()`.
"""

from __future__ import annotations
from enum import Enum

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.participant.participant import Participant


class UserType(Enum):
    """Represents different types of users (humans vs. simulated users)."""

    HUMAN = 0
    SIMULATOR = 1


class User(Participant):
    """Represents a user."""

    def __init__(self, id: str, type: UserType = UserType.HUMAN) -> None:
        """Initializes the user.

        Args:
            user_id: User ID.
            user_type: User type (default: HUMAN).
        """
        super().__init__(id=id, type=type)

    def receive_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """This method is called each time there is a new agent utterance.


        Args:
            utterance: Agent utterance.
        """
        # TODO: Move input part to Platform.
        text = input("Your response: ")
        response = AnnotatedUtterance(text)
        self._dialogue_manager.register_user_utterance(response)
