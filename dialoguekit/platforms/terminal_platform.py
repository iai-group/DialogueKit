"""Terminal platform.

This platform is used for getting user input and displaying agent responses in
the terminal.
"""

from typing import Type

from dialoguekit.core import Utterance
from dialoguekit.participant import Agent
from dialoguekit.participant.user import User
from dialoguekit.platforms import Platform


class TerminalPlatform(Platform):
    def __init__(
        self, agent_class: Type[Agent], user_id: str = "terminal_user"
    ) -> None:
        """Represents a terminal platform. It handles a single user.

        Args:
            agent_class: The class of the agent.
            user_id: User ID. Defaults to "terminal_user".
        """
        super().__init__(agent_class)
        self._user_id = user_id

    def start(self) -> None:
        """Starts the platform."""
        self.connect(self._user_id)
        user: User = self._active_users[self._user_id]
        while True:
            if not user.ready_for_input:
                break
            text = input("USER:  ")
            self.message(self._user_id, text)
        self.disconnect(self._user_id)

    def display_agent_utterance(
        self, utterance: Utterance, agent_id: str, user_id: str = None
    ) -> None:
        """Displays an agent utterance.

        Args:
            utterance: An instance of Utterance.
            agent_id: Agent ID.
            user_id: User ID of the recipient. Defaults to None.
        """
        print(f"AGENT: {utterance.text}")

    def display_user_utterance(
        self, utterance: Utterance, user_id: str
    ) -> None:
        """Displays a user utterance.

        Args:
            utterance: An instance of Utterance.
            user_id: User ID.
        """
        pass
