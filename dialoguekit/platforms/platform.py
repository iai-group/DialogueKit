"""The Platform facilitates displaying of the conversation."""

from abc import ABC, abstractmethod
from typing import Callable

from dialoguekit.core.utterance import Utterance


class Platform(ABC):
    def __init__(self):
        """Represents a platform."""
        self._user_callback: Callable[[str], None] = None

    def register_user_callback(self, callback: Callable[[str], None]) -> None:
        """Registers a callback function to be called on user input.

        Args:
            callback: Function to call on user input
        """
        self._user_callback = callback

    @abstractmethod
    def listen_for_user_input(self) -> None:
        """Listens for the user input.

        Args:
            callback: Function to call on user input
        """
        raise NotImplementedError

    @abstractmethod
    def display_agent_utterance(self, utterance: Utterance) -> None:
        """Displays an agent utterance.

        Args:
            utterance: An instance of Utterance.
        """
        raise NotImplementedError

    @abstractmethod
    def display_user_utterance(self, utterance: Utterance) -> None:
        """Diplays a user utterance.

        Args:
            utterance: An instance of Utterance.
        """
        raise NotImplementedError
