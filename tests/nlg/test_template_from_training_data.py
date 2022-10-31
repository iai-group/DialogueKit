"""Tests for extracting templates from training data."""

from dialoguekit.core import AnnotatedUtterance, Annotation, Intent
from dialoguekit.nlg.template_from_training_data import (
    _replace_slot_with_placeholder,
    build_template_from_instances,
    extract_utterance_template,
)
from dialoguekit.nlu import SatisfactionClassifierSVM
from dialoguekit.participant import DialogueParticipant

ANNOTATED_DIALOGUE_FILE = "tests/data/annotated_dialogues.json"


def test_build_template_from_instances_default():
    """Tests if overriding works correctly."""
    utterances = [
        AnnotatedUtterance(
            text="Test Utterance 1-1",
            intent=Intent(label="Test1"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-2",
            intent=Intent(label="Test1"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-3",
            intent=Intent(label="Test1"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-1",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-2",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-3",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert template
    assert len(template.keys()) == 2
    assert len(template[Intent("Test1")]) == 3


def test_build_template_from_instances_no_intents():
    """Tests if exception gets raised if length is missmatched."""
    utterances = [
        AnnotatedUtterance(
            text="Test Utterance 1-1", participant=DialogueParticipant.AGENT
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-2", participant=DialogueParticipant.AGENT
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-3", participant=DialogueParticipant.AGENT
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-1", participant=DialogueParticipant.AGENT
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-2", participant=DialogueParticipant.AGENT
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-3", participant=DialogueParticipant.AGENT
        ),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert len(template) == 0


def test_build_template_from_instances_skip_no_intent():
    """Tests if Utterance without Intents gets skipped."""
    utterances = [
        AnnotatedUtterance(text="Skip", participant=DialogueParticipant.AGENT),
        AnnotatedUtterance(
            text="Test Utterance 1-1",
            intent=Intent(label="Test1"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-2",
            intent=Intent(label="Test1"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-1",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-2",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-3",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert template
    assert "Skip" not in [
        utterance
        for utterances in template.values()
        for utterance in utterances
    ]


def test_build_template_from_instances_duplicate_deletion():
    """Tests if duplicate Utterance for same Intent gets removed."""
    utterances = [
        AnnotatedUtterance(text="Skip", participant=DialogueParticipant.AGENT),
        AnnotatedUtterance(
            text="Test Utterance 1-1",
            intent=Intent(label="Test1"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-1",
            intent=Intent(label="Test1"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-1",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-2",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-3",
            intent=Intent(label="Test2"),
            participant=DialogueParticipant.AGENT,
        ),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert template
    assert len(template[Intent("Test1")]) == 1


def test_replace_slot_with_placeholder():
    """Tests placeholder replacement."""
    # Given
    a1 = AnnotatedUtterance(
        text="I like action or fantasy movies.",
        participant=DialogueParticipant.AGENT,
    )
    a1.add_annotation(Annotation(slot="GENRE", value="action"))
    a1.add_annotation(Annotation(slot="GENRE", value="fantasy"))

    a2 = AnnotatedUtterance(
        text="How about old street?", participant=DialogueParticipant.AGENT
    )
    a2.add_annotation(Annotation(slot="TITLE", value="old street"))
    annotated_utterances = [
        (a1, "I like {GENRE} or {GENRE} movies."),
        (a2, "How about {TITLE}?"),
    ]

    for utterance, expected_text in annotated_utterances:
        _replace_slot_with_placeholder(utterance)
        assert utterance.text == expected_text


def test_extract_utterance_template():
    """Tests template extraction."""
    templates = extract_utterance_template(ANNOTATED_DIALOGUE_FILE)
    from pprint import pprint

    pprint(templates)
    assert templates
    assert set(templates.get(Intent("COMPLETE"))) == set(
        [
            AnnotatedUtterance(
                text="thank you",
                intent=Intent(label="COMPLETE"),
                participant=DialogueParticipant.AGENT,
            ),
            AnnotatedUtterance(
                text="/exit",
                intent=Intent(label="COMPLETE"),
                participant=DialogueParticipant.AGENT,
            ),
            AnnotatedUtterance(
                text="I would like to quit now.",
                intent=Intent(label="COMPLETE"),
                participant=DialogueParticipant.AGENT,
            ),
        ]
    )

    test_annotation = AnnotatedUtterance(
        text="something like the {TITLE}",
        intent=Intent(label="REVEAL.EXPAND"),
        annotations=[Annotation(slot="TITLE", value="")],
        participant=DialogueParticipant.AGENT,
    )

    assert templates.get(Intent("REVEAL.EXPAND")) == [test_annotation]


def test_extract_utterance_template_with_satisfaction():
    """Tests tempalte generation with satisfaction."""
    templates = extract_utterance_template(
        ANNOTATED_DIALOGUE_FILE,
        satisfaction_classifier=SatisfactionClassifierSVM(),
    )

    for annotated_utterance in templates[Intent("DISCLOSE")]:
        assert 0 < annotated_utterance.metadata.get("satisfaction") <= 4
