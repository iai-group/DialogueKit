"""Test the classes in flask_socket_platform.py."""

from unittest import mock

import pytest

from dialoguekit.core import AnnotatedUtterance, Intent, Utterance
from dialoguekit.participant import DialogueParticipant
from dialoguekit.platforms import FlaskSocketPlatform
from dialoguekit.platforms.flask_socket_platform import ChatNamespace, Message
from sample_agents import ParrotAgent


class TestFlaskSocketPlatform(FlaskSocketPlatform):
    def __init__(self, *args, **kwargs):
        """Initialize the platform with mock methods."""
        super().__init__(*args, **kwargs)
        self.connect = mock.MagicMock(spec=self.connect)
        self.disconnect = mock.MagicMock(spec=self.disconnect)
        self.message = mock.MagicMock(spec=self.message)
        self.feedback = mock.MagicMock(spec=self.feedback)


@pytest.fixture
def platform():
    """Create a FlaskSocketPlatform with a ParrotAgent."""
    platform = TestFlaskSocketPlatform(agent_class=ParrotAgent)
    platform.app.config["TESTING"] = True
    yield platform


@pytest.fixture
def socket_client(platform):
    """Create a test client for socketio."""
    platform.socketio.on_namespace(ChatNamespace("/", platform))
    yield platform.socketio.test_client(
        platform.app,
        flask_test_client=platform.app.test_client(),
    )


def test_message_from_utterance():
    """Test that a Message is created from an Utterance."""
    text = "Hello, world!"
    utterance = Utterance(text, DialogueParticipant.AGENT)

    message = Message.from_utterance(utterance)

    assert message.text == text
    assert message.intent is None


def test_message_from_annotated_utterance():
    """Test that a Message is created from an AnnotatedUtterance."""
    text = "Hello, world!"
    intent = "greeting"
    annotated_utterance = AnnotatedUtterance(
        text, DialogueParticipant.AGENT, intent=Intent(intent)
    )

    annotated_message = Message.from_utterance(annotated_utterance)

    assert annotated_message.text == text
    assert annotated_message.intent == intent


def test_connection(platform, socket_client):
    """Test that a connection is established."""
    assert socket_client.is_connected()

    platform.connect.assert_called_once()
    platform.disconnect.assert_not_called()


def test_disconnection(platform, socket_client):
    """Test platform disconnects the user when client disconnects."""
    socket_client.disconnect()

    platform.connect.assert_called_once()
    platform.disconnect.assert_called_once()


def test_receive_message(platform, socket_client):
    """Test platform receives a message from the client."""
    socket_client.send({"message": "Hello!"})

    platform.message.assert_called_once_with(mock.ANY, "Hello!")


def test_receive_feedback(platform, socket_client):
    """Test platform receives feedback from the client."""
    feedback_data = {"utterance_id": 5, "value": 1}
    socket_client.emit("feedback", {"feedback": feedback_data})

    platform.feedback.assert_called_once_with(mock.ANY, **feedback_data)

    received = socket_client.get_received()
    assert len(received) == 1
    assert received[0]["args"]["info"] == "Feedback received"


@mock.patch("flask_socketio.SocketIO.send")
def test_display_agent_utterance(send, platform):
    """Test that the agent utterance is sent to the user."""
    user_id = "test_user_id"
    text = "Hello, I'm an agent!"
    utterance = Utterance(text, DialogueParticipant.AGENT)

    platform.display_agent_utterance(user_id, utterance)
    send.assert_called_once_with(
        {
            "recipient": user_id,
            "message": {"text": text, "intent": None},
        },
        room=user_id,
    )
