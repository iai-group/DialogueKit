"""Tests for the Dialogue class."""

import calendar
import datetime

import pytest

from dialoguekit.core import (
    AnnotatedUtterance,
    Annotation,
    Dialogue,
    Intent,
    Utterance,
)
from dialoguekit.participant import DialogueParticipant


# Dialogue history object to be shared across multiple test cases.
@pytest.fixture(scope="module")
def dialogue_history_1() -> Dialogue:
    """Dialogue with unannotated utterances fixture."""
    agent_id = "agent-001"
    user_id = "USR01"
    conversation_id = "CNV1"
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

    dialogue_history = Dialogue(agent_id, user_id, conversation_id)
    for utterance in utterances:
        dialogue_history.add_utterance(utterance)
    return dialogue_history


@pytest.fixture(scope="module")
def dialogue_history_2() -> Dialogue:
    """Dialogue with annotated utterances and metadata fixture."""
    agent_id = "agent-002"
    user_id = "USR02"
    conversation_id = "CNV1"
    agent_utterance_1 = AnnotatedUtterance(
        "Hello",
        participant=DialogueParticipant.AGENT,
        intent=Intent("GREETINGS"),
    )
    user_utterance_1 = AnnotatedUtterance(
        "Hi", participant=DialogueParticipant.USER, intent=Intent("GREETINGS")
    )
    agent_utterance_2 = AnnotatedUtterance(
        "What is your favorite color?",
        participant=DialogueParticipant.AGENT,
        intent=Intent("ELICIT"),
        annotations=[Annotation("COLOR", "color")],
    )
    utterances = [
        agent_utterance_1,
        user_utterance_1,
        agent_utterance_2,
    ]

    dialogue_history = Dialogue(agent_id, user_id, conversation_id)
    dialogue_history.metadata.update(
        {"description": "Dialogue fixture for testing"}
    )
    for utterance in utterances:
        dialogue_history.add_utterance(utterance)

    return dialogue_history


@pytest.fixture(scope="module")
def dialogue_history_3() -> Dialogue:
    """Empty dialogue fixture."""
    return Dialogue("agent-003", "USR03", "CNV1")


def test_initialization():
    """Tests dialogue initialization."""
    agent_id = "agent-002"
    user_id = "USR02"
    conversation_id = "CNV1"
    dialogue_1 = Dialogue(agent_id, user_id, conversation_id)
    assert dialogue_1.conversation_id == conversation_id
    dialogue_2 = Dialogue(agent_id, user_id)
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    assert dialogue_2.conversation_id == f"{agent_id}-{user_id}-{str(utc_time)}"


def test_ids(dialogue_history_1: Dialogue) -> None:
    """Tests dialogue parameters.

    Args:
        dialogue_history_1: Test Dialogue object.
    """
    assert dialogue_history_1.agent_id == "agent-001"
    assert dialogue_history_1.user_id == "USR01"


def test_utterances(dialogue_history_1: Dialogue) -> None:
    """Tests Dialogue utterances.

    Args:
        dialogue_history_1: Test Dialogue object.
    """
    assert len(dialogue_history_1.utterances) == len(
        dialogue_history_1.utterances
    )
    assert dialogue_history_1.utterances[0].text == "Hello"
    assert dialogue_history_1.utterances[0].utterance_id == "CNV1_agent-001_0"
    assert (
        dialogue_history_1.utterances[0].participant
        == DialogueParticipant.AGENT
    )
    assert (
        dialogue_history_1.utterances[1].participant == DialogueParticipant.USER
    )
    assert dialogue_history_1.utterances[1].text == "Hi"
    assert dialogue_history_1.utterances[1].utterance_id == "CNV1_USR01_1"
    assert (
        dialogue_history_1.utterances[4].participant
        == DialogueParticipant.AGENT
    )


def test_add_utterance() -> None:
    """Tests adding utterance to dialogue history."""
    agent_id = "agent-002"
    user_id = "USR02"
    conversation_id = "CNV1"
    utterance_no_id = AnnotatedUtterance(
        "Hi", participant=DialogueParticipant.USER, intent=Intent("GREETINGS")
    )
    utterance_with_id = AnnotatedUtterance(
        "Hi",
        utterance_id="u_1",
        participant=DialogueParticipant.AGENT,
        intent=Intent("GREETINGS"),
    )
    dialogue_history = Dialogue(agent_id, user_id, conversation_id)

    dialogue_history.add_utterance(utterance_no_id)
    dialogue_history.add_utterance(utterance_with_id)

    assert dialogue_history.utterances[0].utterance_id == "CNV1_USR02_0"
    assert dialogue_history.utterances[1].utterance_id == "u_1"


def test_to_dict_d1(dialogue_history_1: Dialogue) -> None:
    """Tests dialogue export to dictionary.

    Args:
        dialogue_history_1: Test Dialogue object 1.
        dialogue_history_2: Test Dialogue object 2.
    """
    dialogue_dict_1 = dialogue_history_1.to_dict()

    assert dialogue_dict_1.get("agent") == "agent-001"
    assert dialogue_dict_1.get("user") == "USR01"
    assert dialogue_dict_1.get("conversation ID") == "CNV1"
    assert dialogue_dict_1.get("metadata") is None
    assert len(dialogue_dict_1.get("conversation")) == 5
    utterance_1 = dialogue_dict_1.get("conversation")[0]
    assert utterance_1["utterance"] == "Hello"
    assert utterance_1["utterance ID"] == "CNV1_agent-001_0"
    assert utterance_1.get("slot_values") is None


def test_to_dict_d2(dialogue_history_2: Dialogue) -> None:
    """Tests dialogue export to dictionary.

    Dialogue has annotations and metadata.

    Args:
        dialogue_history_2: Test Dialogue object 2.
    """
    dialogue_dict_2 = dialogue_history_2.to_dict()

    assert dialogue_dict_2.get("agent") == "agent-002"
    assert dialogue_dict_2.get("user") == "USR02"
    assert dialogue_dict_2.get("metadata") == {
        "description": "Dialogue fixture for testing"
    }
    assert len(dialogue_dict_2.get("conversation")) == 3

    utterances = dialogue_dict_2.get("conversation")
    last_utterance = utterances.pop()

    assert set([(u["intent"], u.get("slot_values")) for u in utterances]) == {
        ("GREETINGS", None)
    }

    assert last_utterance["intent"] == "ELICIT"
    assert last_utterance["slot_values"] == [["COLOR", "color"]]


def test_to_dict_d3(dialogue_history_3: Dialogue) -> None:
    """Tests dialogue export to dictionary.

    Dialogue is empty.

    Args:
        dialogue_history_3: Test Dialogue object 3.
    """
    dialogue_dict_3 = dialogue_history_3.to_dict()

    assert dialogue_dict_3.get("agent") == "agent-003"
    assert dialogue_dict_3.get("user") == "USR03"
    assert dialogue_dict_3.get("metadata") is None
    assert len(dialogue_dict_3.get("conversation")) == 0
    assert len(dialogue_dict_3.keys()) == 4
