"""Tests for extracting templates from training data."""

import pytest

from dialoguekit.nlg.template_from_training_data import (
    replace_slot_with_placeholder,
    extract_utterance_template,
)


ANNOTATED_DIALOGUE_FILE = "tests/data/annotated_dialogues.json"


def test_replace_slot_with_placeholder():
    # Given
    annotated_utterance = [
        (
            "I like action or fantasy movies.",
            [
                ["GENRE", "action"],
                ["GENRE", "fantasy"]
            ],
            "I like {GENRE} or {GENRE} movies.",
        ),
        ("How about old street?", [["TITLE", "old street"]], "How about {TITLE}?"),
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
    assert templates.get("REVEAL.EXPAND") == [
        "something like the {TITLE}\n"
    ]
