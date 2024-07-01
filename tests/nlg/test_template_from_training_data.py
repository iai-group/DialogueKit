"""Tests for extracting templates from training data."""

from dialoguekit.core import AnnotatedUtterance, Intent, SlotValueAnnotation
from dialoguekit.core.dialogue_act import DialogueAct
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
            dialogue_acts=[DialogueAct(Intent("Test1"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-2",
            dialogue_acts=[DialogueAct(Intent("Test1"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-3",
            dialogue_acts=[DialogueAct(Intent("Test1"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-1",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-2",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-3",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 3-1",
            dialogue_acts=[
                DialogueAct(Intent("Test1")),
                DialogueAct(Intent("Test3")),
            ],
            participant=DialogueParticipant.AGENT,
        ),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert template
    assert len(template.keys()) == 3
    assert len(template["Test1"]) == 3
    assert len(template["Test1;Test3"]) == 1


def test_build_template_from_instances_no_intents():
    """Tests if exception gets raised if length is mismatched."""
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
            dialogue_acts=[DialogueAct(Intent("Test1"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-2",
            dialogue_acts=[DialogueAct(Intent("Test1"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-1",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-2",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-3",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
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
            dialogue_acts=[DialogueAct(Intent("Test1"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 1-1",
            dialogue_acts=[DialogueAct(Intent("Test1"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-1",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-2",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
        AnnotatedUtterance(
            text="Test Utterance 2-3",
            dialogue_acts=[DialogueAct(Intent("Test2"))],
            participant=DialogueParticipant.AGENT,
        ),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert template
    assert len(template["Test1"]) == 1


def test_replace_slot_with_placeholder():
    """Tests placeholder replacement."""
    # Given
    a1 = AnnotatedUtterance(
        text="I like action or fantasy movies.",
        participant=DialogueParticipant.AGENT,
    )
    a1.add_dialogue_acts(
        [
            DialogueAct(
                annotations=[
                    SlotValueAnnotation(slot="GENRE", value="action"),
                    SlotValueAnnotation(slot="GENRE", value="fantasy"),
                ]
            )
        ]
    )

    a2 = AnnotatedUtterance(
        text="How about old street?", participant=DialogueParticipant.AGENT
    )
    a2.add_dialogue_acts(
        [
            DialogueAct(
                annotations=[
                    SlotValueAnnotation(slot="TITLE", value="old street")
                ]
            )
        ]
    )
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
    assert set(templates.get("COMPLETE")) == set(
        [
            AnnotatedUtterance(
                text="thank you",
                dialogue_acts=[DialogueAct(Intent("COMPLETE"))],
                participant=DialogueParticipant.AGENT,
            ),
            AnnotatedUtterance(
                text="/exit",
                dialogue_acts=[DialogueAct(Intent("COMPLETE"))],
                participant=DialogueParticipant.AGENT,
            ),
            AnnotatedUtterance(
                text="I would like to quit now.",
                dialogue_acts=[DialogueAct(Intent("COMPLETE"))],
                participant=DialogueParticipant.AGENT,
            ),
        ]
    )

    test_annotation = AnnotatedUtterance(
        text="something like the {TITLE}",
        dialogue_acts=[
            DialogueAct(
                Intent("REVEAL.EXPAND"),
                [SlotValueAnnotation(slot="TITLE")],
            )
        ],
        participant=DialogueParticipant.AGENT,
    )

    assert templates.get("REVEAL.EXPAND") == [test_annotation]


def test_extract_utterance_template_with_satisfaction():
    """Tests template generation with satisfaction."""
    templates = extract_utterance_template(
        ANNOTATED_DIALOGUE_FILE,
        satisfaction_classifier=SatisfactionClassifierSVM(),
    )

    for annotated_utterance in templates["DISCLOSE"]:
        assert 0 < annotated_utterance.metadata.get("satisfaction") <= 4
