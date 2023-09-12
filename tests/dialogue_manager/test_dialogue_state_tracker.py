"""Tests for the DialogueStateTracker class."""


import pytest

from dialoguekit.core.intent import Intent
from dialoguekit.dialogue_manager.dialogue_state_tracker import (
    AnnotatedUtterance,
    Annotation,
    DialogueParticipant,
    DialogueStateTracker,
)


@pytest.fixture
def annotated_utterance() -> AnnotatedUtterance:
    """Return an annotated utterance."""
    return AnnotatedUtterance(
        "Hello",
        DialogueParticipant.USER,
        intent=Intent("greeting"),
        annotations=[Annotation("name", "John")],
    )


def test_initial_state() -> None:
    """Test that the initial state is correct."""
    tracker = DialogueStateTracker()
    state = tracker.get_state()
    assert state.history == []
    assert state.last_user_intent is None
    assert state.slots == {}
    assert state.turn_count == 0


def test_agent_participant(annotated_utterance: AnnotatedUtterance) -> None:
    """Test that the agent participant is updated when the user utterance
    contains annotations.

    Args:
        annotated_utterance: Annotated utterance.
    """
    tracker = DialogueStateTracker()
    agent_utterance = AnnotatedUtterance(
        "Hi, how can I assist you?",
        DialogueParticipant.AGENT,
        intent=Intent("offer_help"),
        annotations=[],
    )

    tracker.update(annotated_utterance)
    assert tracker.get_state().last_user_intent == Intent("greeting")
    assert tracker.get_state().turn_count == 1

    tracker.update(agent_utterance)
    assert tracker.get_state().last_user_intent == Intent("greeting")
    assert tracker.get_state().turn_count == 1
    assert tracker.get_state().history[-1] == agent_utterance


def test_update_history(annotated_utterance: AnnotatedUtterance) -> None:
    """Test that the history is updated when the user utterance contains
    annotations.

    Args:
        annotated_utterance: Annotated utterance.
    """
    tracker = DialogueStateTracker()
    tracker.update(annotated_utterance)
    assert tracker.get_state().history == [annotated_utterance]


def test_update_intent(annotated_utterance: AnnotatedUtterance) -> None:
    """Test that the last user intent is updated when the user utterance
    contains annotations.

    Args:
        annotated_utterance: Annotated utterance.
    """
    tracker = DialogueStateTracker()
    tracker.update(annotated_utterance)
    assert tracker.get_state().last_user_intent == Intent("greeting")


def test_update_slots(annotated_utterance: AnnotatedUtterance) -> None:
    """Test that the slots are updated when the user utterance contains
    annotations.

    Args:
        annotated_utterance: Annotated utterance.
    """
    tracker = DialogueStateTracker()
    tracker.update(annotated_utterance)
    assert tracker.get_state().slots == {"name": [Annotation("name", "John")]}


def test_turn_count(annotated_utterance: AnnotatedUtterance) -> None:
    """Test that the turn count is incremented when the user and agent have
    both acted.

    Args:
        annotated_utterance: Annotated utterance.
    """
    tracker = DialogueStateTracker()

    annotated_utterance_2 = AnnotatedUtterance(
        "How are you?",
        DialogueParticipant.USER,
        Intent("ask_health"),
        annotations=[],
    )
    tracker.update(annotated_utterance)
    tracker.update(annotated_utterance_2)
    assert tracker.get_state().turn_count == 2
