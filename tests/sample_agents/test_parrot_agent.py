"""Tests for ParrotAgent."""
import io
import sys

import pytest

from dialoguekit.connector.dialogue_connector import DialogueConnector
from dialoguekit.participant.agent import AgentType
from dialoguekit.participant.user import User, UserType
from dialoguekit.platforms.platform import Platform
from sample_agents.parrot_agent import ParrotAgent


@pytest.fixture
def user() -> User:
    """User fixture."""
    return User("TestUser", user_type=UserType.SIMULATOR)


@pytest.fixture
def agent() -> ParrotAgent:
    """Parrot agent fixture."""
    agent = ParrotAgent("TestParrotAgent")
    assert agent.id == "TestParrotAgent"
    assert agent._agent_type == AgentType.BOT
    return agent


@pytest.fixture
def connector(user: User, agent: ParrotAgent) -> DialogueConnector:
    """Dialogue connector fixture."""
    connector = DialogueConnector(
        agent, user, Platform(), save_dialogue_history=False
    )
    return connector


def test_greetings(connector: DialogueConnector, monkeypatch) -> None:
    """Test for welcome and goodbye methods."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("EXIT"))
    connector.start()
    assert len(connector.dialogue_history.utterances) == 3
    assert (
        connector.dialogue_history.utterances[0].text
        == "Hello, I'm Parrot. What can I help u with?"
    )
    assert (
        connector.dialogue_history.utterances[-1].text
        == "It was nice talking to you. Bye"
    )
