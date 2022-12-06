"""Tests for ParrotAgent."""
import io
import sys

import pytest

from dialoguekit.agent.agent import AgentType
from dialoguekit.connector.dialogue_connector import DialogueConnector
from dialoguekit.platforms.platform import Platform
from dialoguekit.user.user import User, UserType
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
def dc(user: User, agent: ParrotAgent) -> DialogueConnector:
    """Dialogue connector fixture."""
    dc = DialogueConnector(agent, user, Platform(), save_dialogue_history=False)
    return dc


def test_greetings(dc: DialogueConnector, monkeypatch) -> None:
    """Test for welcome and goodbye methods."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("EXIT"))
    dc.start()
    assert len(dc.dialogue_history.utterances) == 3
    assert (
        dc.dialogue_history.utterances[0].text
        == "Hello, I'm Parrot. What can I help u with?"
    )
    assert (
        dc.dialogue_history.utterances[-1].text
        == "It was nice talking to you. Bye"
    )
