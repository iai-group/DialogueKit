"""Tests for ParrotAgent."""
import io
import sys

import pytest
from dialoguekit.agent.agent import AgentType
from dialoguekit.manager.dialogue_manager import DialogueManager
from dialoguekit.platforms.platform import Platform
from dialoguekit.user.user import User, UserType

from sample_agents.parrot_agent import ParrotAgent


@pytest.fixture
def user() -> User:
    return User("TestUser", user_type=UserType.SIMULATOR)


@pytest.fixture
def agent() -> ParrotAgent:
    agent = ParrotAgent("TestParrotAgent")
    assert agent.id == "TestParrotAgent"
    assert agent._agent_type == AgentType.BOT
    return agent


@pytest.fixture
def dm(user: User, agent: ParrotAgent) -> DialogueManager:
    dm = DialogueManager(agent, user, Platform(), save_dialogue_history=False)
    return dm


def test_greetings(dm: DialogueManager, monkeypatch) -> None:
    """Test for welcome and goodbye methods."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("EXIT"))
    dm.start()
    assert len(dm.dialogue_history.utterances) == 3
    assert (
        dm.dialogue_history.utterances[0].text
        == "Hello, I'm Parrot. What can I help u with?"
    )
    assert (
        dm.dialogue_history.utterances[-1].text
        == "It was nice talking to you. Bye"
    )
