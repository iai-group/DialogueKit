"""Tests for ParrotAgent."""
import io
import sys

import pytest

from dialoguekit.platforms import TerminalPlatform
from sample_agents.parrot_agent import ParrotAgent


@pytest.fixture
def platform() -> TerminalPlatform:
    """Dialogue connector fixture."""
    platform = TerminalPlatform(ParrotAgent)
    return platform


def test_greetings(platform: TerminalPlatform, monkeypatch) -> None:
    """Test for welcome and goodbye methods."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("EXIT"))
    platform.start()
    connector = platform.get_user("terminal_user").get_dialogue_connector()
    assert len(connector.dialogue_history.utterances) == 3
    assert (
        connector.dialogue_history.utterances[0].text
        == "Hello, I'm Parrot. What can I help u with?"
    )
    assert (
        connector.dialogue_history.utterances[-1].text
        == "It was nice talking to you. Bye"
    )
