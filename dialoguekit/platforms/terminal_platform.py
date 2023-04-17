"""Terminal platform.

This platform is used for getting user input and displaying agent
responses in the terminal.
"""
from typing import Type

from dialoguekit.core import Utterance
from dialoguekit.participant import Agent
from dialoguekit.participant.user import User
from dialoguekit.platforms import Platform


class TerminalPlatform(Platform):
    def __init__(self, agent_class: Type[Agent], user_id: str = None) -> None:
        """Represents a terminal platform. It handles a single user.

        Args:
            agent_class: The class of the agent.
            user_id: User ID (default: terminal_user).
        """
        super().__init__(agent_class)
        self._user_id = user_id or "terminal_user"

    def start(self) -> None:
        """Starts the platform."""
        self.connect(self._user_id)
        user: User = self._active_users[self._user_id]
        while True:
            if not user.ready_for_input:
                break
            text = input()
            self.message(self._user_id, text)

    def display_agent_utterance(
        self, user_id: str, utterance: Utterance
    ) -> None:
        """Displays an agent utterance.

        Args:
            utterance: An instance of Utterance.
        """
        print(f"AGENT: {utterance.text}")

    def display_user_utterance(
        self, user_id: str, utterance: Utterance
    ) -> None:
        """Displays a user utterance.

        Args:
            utterance: An instance of Utterance.
        """
        print(f"USER:  {utterance.text}\n")
