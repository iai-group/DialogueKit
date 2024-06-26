"""Tests for the Utterance class."""

from dialoguekit.core import AnnotatedUtterance, Intent
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.participant import DialogueParticipant


def test_utterance_text():
    """Tests setting text."""
    u = AnnotatedUtterance("Hello world", DialogueParticipant.USER)
    assert u.text == "Hello world"


def test_comparison():
    """Tests object comparison."""
    u1 = AnnotatedUtterance(
        "Test1",
        dialogue_acts=[DialogueAct(Intent("1"))],
        participant=DialogueParticipant.AGENT,
    )
    u2 = u1
    assert u1 == u2

    u3 = AnnotatedUtterance(
        "Test1",
        dialogue_acts=[DialogueAct(Intent("1"))],
        participant=DialogueParticipant.AGENT,
    )
    assert u1 == u3

    # Test Text difference
    u1 = AnnotatedUtterance(
        text="Test1",
        dialogue_acts=[DialogueAct(Intent("1"))],
        participant=DialogueParticipant.AGENT,
    )
    u2 = AnnotatedUtterance(
        text="Test2",
        dialogue_acts=[DialogueAct(Intent("1"))],
        participant=DialogueParticipant.AGENT,
    )
    assert u1 != u2

    # Test Dialogue act difference
    u1 = AnnotatedUtterance(
        text="Test1",
        dialogue_acts=[DialogueAct(Intent("1")), DialogueAct(Intent("2"))],
        participant=DialogueParticipant.AGENT,
    )
    u2 = AnnotatedUtterance(
        text="Test1",
        dialogue_acts=[DialogueAct(Intent("2"))],
        participant=DialogueParticipant.AGENT,
    )
    assert u1 != u2

    # Test Annotation difference
    u1 = AnnotatedUtterance(
        text="Test1",
        dialogue_acts=[DialogueAct(Intent("1"))],
        annotations=[Annotation("slot", "value1")],
        participant=DialogueParticipant.AGENT,
    )
    u2 = AnnotatedUtterance(
        text="Test1",
        dialogue_acts=[DialogueAct(Intent("1"))],
        annotations=[Annotation("slot", "value2")],
        participant=DialogueParticipant.AGENT,
    )
    assert u1 != u2


def test_get_intents() -> None:
    """Tests getting intents from utterance."""
    u1 = AnnotatedUtterance(
        text="Test1",
        dialogue_acts=[DialogueAct(Intent("1")), DialogueAct(Intent("2"))],
        participant=DialogueParticipant.AGENT,
    )

    assert u1.get_intents() == [Intent("1"), Intent("2")]


def test_add_dialogue_acts() -> None:
    """Tests adding dialogue acts to utterance."""
    u1 = AnnotatedUtterance(
        text="Test1",
        dialogue_acts=[DialogueAct(Intent("1"))],
        participant=DialogueParticipant.AGENT,
    )
    u1.add_dialogue_acts(
        [DialogueAct(Intent("2"), [Annotation("year", "2023")])]
    )

    assert u1.get_intents() == [Intent("1"), Intent("2")]
    assert u1.get_dialogue_act_annotations() == [Annotation("year", "2023")]
