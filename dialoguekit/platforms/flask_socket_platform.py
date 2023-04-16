"""The Platform facilitates displaying of the conversation."""
import logging
from typing import Any, Dict, Type

from flask import Flask, request
from flask_socketio import Namespace, SocketIO, send

from dialoguekit.connector import DialogueConnector
from dialoguekit.core import Utterance
from dialoguekit.participant import Agent, User
from dialoguekit.platforms.platform import Platform

logger = logging.getLogger(__name__)


class FlaskSocketPlatform(Platform):
    def __init__(self, agent_class: Type[Agent]) -> None:
        """Represents a platform.

        Args:
            agent_class: The class of the agent.
        """
        if not issubclass(agent_class, Agent):
            raise ValueError("agent_class must be a subclass of Agent")
        self._agent_class = agent_class
        self._active_users: Dict[str, User] = {}
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

    def start(self) -> None:
        """Starts the platform.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        self.socketio.on_namespace(ChatNamespace("/", self))
        self.socketio.run(self.app, host="127.0.0.1", port="5000")

    def display_agent_utterance(
        self, user_id: str, utterance: Utterance
    ) -> None:
        """Emits agent utterance to the client.

        Args:
            user_id: User ID.
            utterance: An instance of Utterance.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        send(utterance.text, room=user_id)

    def display_user_utterance(
        self, user_id: str, utterance: Utterance
    ) -> None:
        """Emits user utterance to the client.

        Args:
            user_id: User ID.
            utterance: An instance of Utterance.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        send(utterance.text, room=user_id)

    def get_new_agent(self) -> Agent:
        """Returns a new instance of the agent.

        Returns:
            Agent.
        """
        return self._agent_class("agent")

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
        dialogue_connector = user.get_dialogue_connector()
        dialogue_connector.close()

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
        self.get_user(user_id).handle_utterance_feedback(utterance_id, value)


class ChatNamespace(Namespace):
    def __init__(self, namespace: str, platform: FlaskSocketPlatform) -> None:
        """Represents a namespace.

        Args:
            namespace: Namespace.
            controller_flask: Controller.
        """
        super().__init__(namespace)
        self._platform = platform

    def on_connect(self, data: Dict[str, Any]) -> None:
        """Connects client to server.

        Args:
            data: Data received from client.
        """
        user_id = request.sid
        self._platform.connect(user_id)
        logger.info(f"Client connected; user_id: {user_id}")

    def on_disconnect(self) -> None:
        """Disconnects client from server."""
        user_id = request.sid
        self._platform.disconnect(user_id)
        logger.info(f"Client disconnected; user_id: {user_id}")

    def on_message(self, data: dict) -> None:
        """Receives message from client and sends response.

        Args:
            data: Data received from client.
        """
        self._platform.message(request.sid, data["message"])
        logger.info(f"Message received: {data}")

    def on_feedback(self, data: dict) -> None:
        """Receives feedback from client.

        Args:
            data: Data received from client.
        """
        logger.info(f"Feedback received: {data}")
        # TODO: Implement feedback
        # issue: https://github.com/iai-group/DialogueKit/issues/219
        send({"info": "Feedback received"})
