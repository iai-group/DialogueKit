"""The Platform facilitates displaying of the conversation."""

from abc import ABC, abstractmethod
from typing import Dict, Type

from dialoguekit.connector import DialogueConnector
from dialoguekit.core import Utterance
from dialoguekit.participant import Agent, User


class Platform(ABC):
    def __init__(self, agent_class: Type[Agent]) -> None:
        """Represents a platform.

        Args:
            agent_class: The class of the agent.
        """
        if not issubclass(agent_class, Agent):
            raise ValueError("agent_class must be a subclass of Agent")
        self._agent_class = agent_class
        self._active_users: Dict[str, User] = {}

    @abstractmethod
    def start(self) -> None:
        """Starts the platform.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def display_agent_utterance(
        self, utterance: Utterance, agent_id: str, user_id: str
    ) -> None:
        """Displays an agent utterance.

        Considering that an agent can interact with multiple users, the
        user_id is provided to identify the recipient.

        Args:
            utterance: An instance of Utterance.
            agent_id: Agent ID.
            user_id: User ID of the recipient.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def display_user_utterance(
        self, utterance: Utterance, user_id: str
    ) -> None:
        """Displays a user utterance.

        Args:
            utterance: An instance of Utterance.
            user_id: User ID.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    def get_new_agent(self) -> Agent:
        """Returns a new instance of the agent.

        Returns:
            Agent.
        """
        return self._agent_class(self._agent_class.__name__)

    def get_user(self, user_id: str) -> User:
        """Returns the user.

        Args:
            user_id: User ID.

        Returns:
            User.
        """
        return self._active_users.get(user_id)

    def connect(self, user_id: str) -> None:
        """Connects a user to an agent.

        Args:
            user_id: User ID.
        """
        self._active_users[user_id] = User(user_id)
        dialogue_connector = DialogueConnector(
            agent=self.get_new_agent(),
            user=self._active_users[user_id],
            platform=self,
        )
        dialogue_connector.start()

    def disconnect(self, user_id: str) -> None:
        """Disconnects a user from an agent.

        Args:
            user_id: User ID.
        """
        user = self._active_users.pop(user_id)
        user.dialogue_connector.close()

    def message(self, user_id: str, text: str) -> None:
        """Gets called every time there is a new user input.

        Args:
            user_id: User ID.
            text: User input.
        """
        self.get_user(user_id).handle_input(text)

    def feedback(self, user_id: str, utterance_id: str, value: int) -> None:
        """Gets called every time there is a new utterance feedback.

        Args:
            user_id: User ID.
            utterance_id: Utterance ID.
            value: Feedback value.
        """
        # Issue: https://github.com/iai-group/DialogueKit/issues/219
        pass
