"""Tests for the Utterance class."""
import pytest
from dialoguekit.core.utterance import Utterance


def test_utterance_text():
    u = Utterance("Hello world")
    assert u.text == "Hello world"


def test_hash():
    u1 = Utterance("Test1")
    try:
        hash(u1)
    except TypeError:
        pytest.fail("Utterance hashing failed")


def test_comparison():
    u1 = Utterance("Test1")
    u2 = u1
    assert u1 == u2

    u3 = Utterance("Test1")
    assert u1 == u3

    # Test Text difference
    u1 = Utterance(text="Test1")
    u2 = Utterance(text="Test2")
    assert u1 != u2
