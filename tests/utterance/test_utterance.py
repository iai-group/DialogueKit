"""Tests for the Utterance class."""

from dialoguekit.utterance.utterance import Utterance


def test_utterance_text():
    u = Utterance("Hello world")
    assert u.text == "Hello world"
