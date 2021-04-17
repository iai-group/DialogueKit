"""Tests for the DialogueHistory class."""

import pytest

from dialoguekit.manager.dialogue_history import (
    DialogueHistory,
    DialogueParticipant,
)
from dialoguekit.utterance.utterance import Utterance

# Dialogue history object to be shared across multiple test cases.
@pytest.fixture
def dialogue_history_1():
    agent_id = "agent-001"
    user_id = "USR01"
    dialogue_history = DialogueHistory(agent_id, user_id)
    dialogue_history.add_agent_utterance(Utterance("Hello"))
    dialogue_history.add_user_utterance(Utterance("Hi"))
    dialogue_history.add_agent_utterance(Utterance("Can I help you?"))
    dialogue_history.add_user_utterance(Utterance("No, thank you. Bye"))
    dialogue_history.add_agent_utterance(Utterance("Bye."))
    return dialogue_history


def test_ids(dialogue_history_1):
    assert dialogue_history_1.agent_id == "agent-001"
    assert dialogue_history_1.user_id == "USR01"


def test_utterances(dialogue_history_1):
    assert len(dialogue_history_1.utterances) == 5
    assert dialogue_history_1.utterances[0]["utterance"].text == "Hello"
    assert (
        dialogue_history_1.utterances[0]["sender"] == DialogueParticipant.AGENT
    )
    assert (
        dialogue_history_1.utterances[1]["sender"] == DialogueParticipant.USER
    )
    assert dialogue_history_1.utterances[1]["utterance"].text == "Hi"
    assert (
        dialogue_history_1.utterances[4]["sender"] == DialogueParticipant.AGENT
    )
