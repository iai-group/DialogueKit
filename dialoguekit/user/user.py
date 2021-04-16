"""Abstract representation of core user-related data and functionality.

For communicating with an agent, the specific user instance needs to be
connected with a DialogueManager by invoking `register_dialogue_manager()`.
"""

from enum import Enum

from dialoguekit.utterance.utterance import Utterance


class UserType(Enum):
    """Represents different types of users (humans vs. simulated users)."""
    HUMAN = 0
    SIMULATOR = 1


class User:
    """Represents a user."""

    def __init__(self, user_type: UserType = UserType.HUMAN) -> None:
        """Initializes the user.

        Args:
            user_type: User type (default: HUMAN).
        """
        self._user_type = user_type
        self._dialogue_manager = None
        # TODO: add user_id, history

    def connect_dialogue_manager(self, dialogue_manager) -> None:
        """Connects the Dialogue Manager instance for the user.

        Args:
            dialogue_manager: A DialogueManager instance.

        TODO: Add type annotation for dialogue_manager.
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
