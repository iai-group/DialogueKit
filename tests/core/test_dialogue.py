"""Tests for the DialogueHistory class."""

import pytest
from dialoguekit.core import Dialogue, Utterance
from dialoguekit.participant import DialogueParticipant


# Dialogue history object to be shared across multiple test cases.
@pytest.fixture(scope="module")
def dialogue_history_1():
    """Tests Dialogue creation."""
    agent_id = "agent-001"
    user_id = "USR01"
    agent_utterance_1 = Utterance(
        "Hello", participant=DialogueParticipant.AGENT
    )
    user_utterance_1 = Utterance("Hi", participant=DialogueParticipant.USER)
    agent_utterance_2 = Utterance(
        "Can I help you?", participant=DialogueParticipant.AGENT
    )
    user_utterance_2 = Utterance(
        "No, thank you. Bye", participant=DialogueParticipant.USER
    )
    agent_utterance_3 = Utterance("Bye.", participant=DialogueParticipant.AGENT)
    utterances = [
        agent_utterance_1,
        user_utterance_1,
        agent_utterance_2,
        user_utterance_2,
        agent_utterance_3,
    ]

    dialogue_history = Dialogue(agent_id, user_id)
    for utterance in utterances:
        dialogue_history.add_utterance(utterance)

    return dialogue_history


def test_ids(dialogue_history_1):
    """Tests dialogue parameters.

    Args:
        dialogue_history_1: Test Dialogue object.
    """
    assert dialogue_history_1.agent_id == "agent-001"
    assert dialogue_history_1.user_id == "USR01"


def test_utterances(dialogue_history_1):
    """Tests Dialogue utterances.

    Args:
        dialogue_history_1: Test Dialogue object.
    """
    assert len(dialogue_history_1.utterances) == len(
        dialogue_history_1.utterances
    )
    assert dialogue_history_1.utterances[0].text == "Hello"
    assert (
        dialogue_history_1.utterances[0].participant
        == DialogueParticipant.AGENT
    )
    assert (
        dialogue_history_1.utterances[1].participant == DialogueParticipant.USER
    )
    assert dialogue_history_1.utterances[1].text == "Hi"
    assert (
        dialogue_history_1.utterances[4].participant
        == DialogueParticipant.AGENT
    )
