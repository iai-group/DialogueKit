"""Tests for extracting templates from training data."""

import pytest
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlg.template_from_training_data import (
    replace_slot_with_placeholder,
    extract_utterance_template,
    build_template_from_instances,
)


ANNOTATED_DIALOGUE_FILE = "tests/data/annotated_dialogues.json"


def test_replace_slot_with_placeholder():
    # Given
    annotated_utterance = [
        (
            "I like action or fantasy movies.",
            [["GENRE", "action"], ["GENRE", "fantasy"]],
            "I like {GENRE} or {GENRE} movies.",
        ),
        (
            "How about old street?",
            [["TITLE", "old street"]],
            "How about {TITLE}?",
        ),
    ]

    for utterance, slot_values, expected_template in annotated_utterance:
        # When
        extracted_template = replace_slot_with_placeholder(
            utterance, slot_values
        )
        # Then
        assert extracted_template == expected_template


def test_extract_utterance_template():
    templates = extract_utterance_template(ANNOTATED_DIALOGUE_FILE)
    from pprint import pprint

    pprint(templates)
    assert templates
    assert templates.get("COMPLETE") == [
        "thank you\n",
        "/exit\n",
        "I would like to quit now.\n",
    ]
    assert templates.get("REVEAL.EXPAND") == ["something like the {TITLE}\n"]


def test_build_template_from_instances_overide():
    """Tests if overriding works correctly."""
    intents = [
        Intent(label="Test1"),
        Intent(label="Test1"),
        Intent(label="Test1"),
        Intent(label="Test2"),
        Intent(label="Test2"),
        Intent(label="Test2"),
    ]
    utterances = [
        Utterance(text="Test Utterance 1-1"),
        Utterance(text="Test Utterance 1-2"),
        Utterance(text="Test Utterance 1-3"),
        Utterance(text="Test Utterance 2-1"),
        Utterance(text="Test Utterance 2-2"),
        Utterance(text="Test Utterance 2-3"),
    ]

    template = build_template_from_instances(
        intents=intents, utterances=utterances
    )
    assert template
    assert len(template.keys()) == 2
    assert len(template["Test1"]) == 3


def test_build_template_from_instances_overide_exception():
    """Tests if exception gets raised if length is missmatched."""
    intents = [
        Intent(label="Test1"),
        Intent(label="Test1"),
        Intent(label="Test1"),
        Intent(label="Test2"),
        Intent(label="Test2"),
    ]
    utterances = [
        Utterance(text="Test Utterance 1-1"),
        Utterance(text="Test Utterance 1-2"),
        Utterance(text="Test Utterance 1-3"),
        Utterance(text="Test Utterance 2-1"),
        Utterance(text="Test Utterance 2-2"),
        Utterance(text="Test Utterance 2-3"),
    ]
    with pytest.raises(ValueError):
        build_template_from_instances(intents=intents, utterances=utterances)


def test_build_template_from_instances_utterace_only():
    """Tests if template gets built with only utterances."""
    utterances = [
        Utterance(text="Test Utterance 1-1", intent=Intent(label="Test1")),
        Utterance(text="Test Utterance 1-2", intent=Intent(label="Test1")),
        Utterance(text="Test Utterance 1-3", intent=Intent(label="Test1")),
        Utterance(text="Test Utterance 2-1", intent=Intent(label="Test2")),
        Utterance(text="Test Utterance 2-2", intent=Intent(label="Test2")),
        Utterance(text="Test Utterance 2-3", intent=Intent(label="Test2")),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert template is not None
    assert len(template.keys()) == 2
    assert len(template["Test1"]) == 3


def test_build_template_from_instances_skip_no_intent():
    """Tests if Utterance without Intents gets skipped."""
    utterances = [
        Utterance(text="Skip"),
        Utterance(text="Test Utterance 1-1", intent=Intent(label="Test1")),
        Utterance(text="Test Utterance 1-2", intent=Intent(label="Test1")),
        Utterance(text="Test Utterance 2-1", intent=Intent(label="Test2")),
        Utterance(text="Test Utterance 2-2", intent=Intent(label="Test2")),
        Utterance(text="Test Utterance 2-3", intent=Intent(label="Test2")),
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
        Utterance(text="Skip"),
        Utterance(text="Test Utterance 1-1", intent=Intent(label="Test1")),
        Utterance(text="Test Utterance 1-1", intent=Intent(label="Test1")),
        Utterance(text="Test Utterance 2-1", intent=Intent(label="Test2")),
        Utterance(text="Test Utterance 2-2", intent=Intent(label="Test2")),
        Utterance(text="Test Utterance 2-3", intent=Intent(label="Test2")),
    ]

    template = build_template_from_instances(utterances=utterances)
    assert template
    assert len(template["Test1"]) == 1
