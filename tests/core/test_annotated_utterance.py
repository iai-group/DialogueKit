"""Tests for the Utterance class."""

from dialoguekit.core import AnnotatedUtterance, Intent
from dialoguekit.participant import DialogueParticipant


def test_utterance_text():
    """Tests setting text."""
    u = AnnotatedUtterance("Hello world", DialogueParticipant.USER)
    assert u.text == "Hello world"


def test_comparison():
    """Tests object comparison."""
    u1 = AnnotatedUtterance(
        "Test1", intent=Intent("1"), participant=DialogueParticipant.AGENT
    )
    u2 = u1
    assert u1 == u2

    u3 = AnnotatedUtterance(
        "Test1", intent=Intent("1"), participant=DialogueParticipant.AGENT
    )
    assert u1 == u3

    # Test Text difference
    u1 = AnnotatedUtterance(
        text="Test1", intent=Intent("1"), participant=DialogueParticipant.AGENT
    )
    u2 = AnnotatedUtterance(
        text="Test2", intent=Intent("1"), participant=DialogueParticipant.AGENT
    )
    assert u1 != u2

    # Test Intent difference
    u1 = AnnotatedUtterance(
        text="Test1", intent=Intent("1"), participant=DialogueParticipant.AGENT
    )
    u2 = AnnotatedUtterance(
        text="Test1", intent=Intent("2"), participant=DialogueParticipant.AGENT
    )
    assert u1 != u2
