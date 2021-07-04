"""Tests for extracting templates from training data."""

import pytest

from dialoguekit.nlg.template_from_training_data import (
    replace_slot_with_placeholder,
    extract_utterance_template,
)


# Sample annotated dialogues to be shared across multiple test cases.
@pytest.fixture
def sample_annotated_dialogue_file():
    return "../../tests/data/annotated_dialogues.json"


# Annotated utterance and its slots.
@pytest.fixture
def annotated_utterance():
    return [
        (
            "I like action or fantasy movies.",
            "GENRE:action;GENRE:fantasy",
            "I like {GENRE} or {GENRE} movies.",
        ),
        ("How about old street?", "TITLE:old street", "How about {TITLE}?"),
    ]


def test_replace_slot_with_placeholder(annotated_utterance):
    for utterance, slot_values, expected_template in annotated_utterance:
        extracted_template = replace_slot_with_placeholder(
            utterance, slot_values
        )
        assert extracted_template == expected_template


def test_extract_utterance_template(sample_annotated_dialogue_file):
    templates = extract_utterance_template(sample_annotated_dialogue_file)
    from pprint import pprint
    pprint(templates)
    assert templates
    assert templates.get("COMPLETE") == [
        "thank you\n",
        "/exit\n",
        "I would like to quit now.\n",
    ]
    assert templates.get("REVEAL.EXPAND") == [
        "something like the {TITLE}\n"
    ]
