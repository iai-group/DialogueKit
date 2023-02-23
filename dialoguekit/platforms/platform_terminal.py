"""The TerminalPlatform enables the presentation of the dialogue on the terminal
and manages user input.
"""

from typing import Callable

from dialoguekit.core.utterance import Utterance
from dialoguekit.platforms.platform import Platform


class TerminalPlatform(Platform):
    def __init__(self):
        """Represents a platform."""
        self._user_callback: Callable[[str], None] = None

    def listen_for_user_input(self) -> None:
        """Listens for the user input.

        Args:
            callback: Function to call on user input
        """
        text = input("Your response: ")
        if self._user_callback:
            self._user_callback(text)

    def display_agent_utterance(self, utterance: Utterance) -> None:
        """Displays an agent utterance.

        Args:
            utterance: An instance of Utterance.
        """
        print(f"AGENT: {utterance.text}")

    def display_user_utterance(self, utterance: Utterance) -> None:
        """Displays a user utterance.

        Args:
            utterance: An instance of Utterance.
        """
        print(f"USER:  {utterance.text}\n")
