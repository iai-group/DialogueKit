"""Test cases for NLG."""

import pytest

from dialoguekit.nlg.nlg import NLG
from tests.nlg.test_template_from_training_data import (
    ANNOTATED_DIALOGUE_FILE,
)


# nlg class shared across tests.
@pytest.fixture
def nlg_class():
    return NLG(ANNOTATED_DIALOGUE_FILE)


def test_generate_utterance_text(nlg_class):
    # A corner case where only one template found, i.e., REVEAL.EXPAND only has something like the {TITLE}.
    sample_response_text = [
        (
            "REVEAL.EXPAND",
            {"TITLE": "A Test Movie Title"},
            "something like the A Test Movie Title\n",
        )
    ]
    for intent, slot_values, expected_response in sample_response_text:
        generated_response = nlg_class.generate_utterance_text(
            intent, slot_values
        )
        assert generated_response == expected_response
