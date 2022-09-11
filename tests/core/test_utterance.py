"""Tests for the Utterance class."""
import pytest
from dialoguekit.core import Utterance
from dialoguekit.participant import DialogueParticipant


def test_utterance_text():
    """Tests setting of the utterance text."""
    u = Utterance("Hello world", participant=DialogueParticipant.AGENT)
    assert u.text == "Hello world"


def test_hash():
    """Tests hashing of the utterance object."""
    u1 = Utterance("Test1", participant=DialogueParticipant.AGENT)
    try:
        hash(u1)
    except TypeError:
        pytest.fail("Utterance hashing failed")


def test_comparison():
    """Tests utterance comparison."""
    u1 = Utterance("Test1", participant=DialogueParticipant.AGENT)
    u2 = u1
    assert u1 == u2

    u3 = Utterance("Test1", participant=DialogueParticipant.AGENT)
    assert u1 == u3

    # Test Text difference
    u1 = Utterance(text="Test1", participant=DialogueParticipant.AGENT)
    u2 = Utterance(text="Test2", participant=DialogueParticipant.AGENT)
    assert u1 != u2
