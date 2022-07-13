"""Tests for the DialogueHistory class."""

import pytest

from dialoguekit.core.dialogue import (
    Dialogue,
    DialogueParticipant,
)
from dialoguekit.core.utterance import Utterance


# Dialogue history object to be shared across multiple test cases.
@pytest.fixture(scope="module")
def dialogue_history_1():
    agent_id = "agent-001"
    user_id = "USR01"
    agent_utterance_1 = "Hello"
    user_utterance_1 = "Hi"
    agent_utterance_2 = "Can I help you?"
    user_utterance_2 = "No, thank you. Bye"
    agent_utterance_3 = "Bye."
    utterances = [
        (DialogueParticipant.AGENT, agent_utterance_1),
        (DialogueParticipant.USER, user_utterance_1),
        (DialogueParticipant.AGENT, agent_utterance_2),
        (DialogueParticipant.USER, user_utterance_2),
        (DialogueParticipant.AGENT, agent_utterance_3),
    ]

    dialogue_history = Dialogue(agent_id, user_id)
    for sender, text in utterances:
        if sender == DialogueParticipant.AGENT:
            dialogue_history.add_agent_utterance(Utterance(text))
        elif sender == DialogueParticipant.USER:
            dialogue_history.add_user_utterance(Utterance(text))

    return dialogue_history


def test_ids(dialogue_history_1):
    assert dialogue_history_1.agent_id == "agent-001"
    assert dialogue_history_1.user_id == "USR01"


def test_utterances(dialogue_history_1):
    assert len(dialogue_history_1.utterances) == len(
        dialogue_history_1.utterances
    )
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
