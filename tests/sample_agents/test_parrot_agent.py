"""Tests for ParrotAgent."""
import io
import sys
from unittest.mock import patch

import pytest

from dialoguekit.platforms import TerminalPlatform
from sample_agents.parrot_agent import ParrotAgent


@pytest.fixture
def platform() -> TerminalPlatform:
    """Dialogue connector fixture."""
    platform = TerminalPlatform(ParrotAgent)
    yield platform


@patch("dialoguekit.connector.dialogue_connector.DialogueConnector.close")
def test_greetings(close, platform: TerminalPlatform, monkeypatch) -> None:
    """Test for welcome and goodbye methods."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("EXIT"))
    platform.start()
    connector = platform.get_user("terminal_user").dialogue_connector
    assert len(connector.dialogue_history.utterances) == 3
    assert (
        connector.dialogue_history.utterances[0].text
        == "Hello, I'm Parrot. What can I help u with?"
    )
    assert (
        connector.dialogue_history.utterances[0].utterance_id
        == "CNV1_TestParrotAgent_0"
    )
    assert (
        connector.dialogue_history.utterances[-1].text
        == "It was nice talking to you. Bye"
    )
    assert (
        connector.dialogue_history.utterances[-1].utterance_id
        == "CNV1_TestParrotAgent_2"
    )
