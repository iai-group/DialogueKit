"""Test cases for NLG."""

import pytest

from dialoguekit.nlg.nlg import NLG
from tests.nlg.test_template_from_training_data import (
    sample_annotated_dialogue_file,
)

# A corner case where only one template found, i.e., REVEAL.EXPAND only has something like the {TITLE}.
@pytest.fixture
def sample_response_text():
    return [
        (
            "REVEAL.EXPAND",
            {"TITLE": "A Test Movie Title"},
            "something like the A Test Movie Title\n",
        )
    ]


# nlg class shared across tests.
@pytest.fixture
def nlg_class(sample_annotated_dialogue_file):
    return NLG(sample_annotated_dialogue_file)


def test_generate_utterance_text(sample_response_text, nlg_class):
    for intent, slot_values, expected_response in sample_response_text:
        generated_response = nlg_class.generate_utterance_text(
            intent, slot_values
        )
        assert generated_response == expected_response
