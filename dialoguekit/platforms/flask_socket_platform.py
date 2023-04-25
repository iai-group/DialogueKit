"""The Platform facilitates displaying of the conversation."""
from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Type

from flask import Flask, request
from flask_socketio import Namespace, SocketIO, emit, send

from dialoguekit.core import AnnotatedUtterance
from dialoguekit.platforms.platform import Platform

if TYPE_CHECKING:
    from dialoguekit.core import Utterance
    from dialoguekit.participant.agent import Agent


logger = logging.getLogger(__name__)


@dataclass
class Message:
    text: str
    intent: str = None

    @classmethod
    def from_utterance(self, utterance: Utterance) -> Message:
        """Converts an utterance to a message.

        Args:
            utterance: An instance of Utterance.

        Returns:
            An instance of Message.
        """
        message = Message(utterance.text)
        if isinstance(utterance, AnnotatedUtterance):
            message.intent = utterance.intent
        return message


@dataclass
class Response:
    recipient: str
    message: Message


class FlaskSocketPlatform(Platform):
    def __init__(self, agent_class: Type[Agent]) -> None:
        """Represents a platform.

        Args:
            agent_class: The class of the agent.
        """
        super().__init__(agent_class)
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

    def start(self, host: str = "127.0.0.1", port: str = "5000") -> None:
        """Starts the platform.

        Args:
            host: Hostname.
            port: Port.
        """
        self.socketio.on_namespace(ChatNamespace("/", self))
        self.socketio.run(self.app, host=host, port=port)

    def display_agent_utterance(
        self, user_id: str, utterance: Utterance
    ) -> None:
        """Emits agent utterance to the client.

        Args:
            user_id: User ID.
            utterance: An instance of Utterance.
        """
        message = Message.from_utterance(utterance)
        emit(
            "message",
            asdict(Response(user_id, message)),
            json=True,
            room=user_id,
        )

    def display_user_utterance(
        self, user_id: str, utterance: Utterance
    ) -> None:
        """Overrides the method in Platform to avoid raising an error.

        This method is not used in FlaskSocketPlatform.

        Args:
            user_id: User ID.
            utterance: An instance of Utterance.
        """
        pass


class ChatNamespace(Namespace):
    def __init__(self, namespace: str, platform: FlaskSocketPlatform) -> None:
        """Represents a namespace.

        Args:
            namespace: Namespace.
            controller_flask: Controller.
        """
        super().__init__(namespace)
        self._platform = platform

    def on_connect(self) -> None:
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
        self._platform.feedback(request.sid, data["feedback"])
        send({"info": "Feedback received"})
