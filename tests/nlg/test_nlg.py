"""Test cases for NLG."""

import pytest
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent

from dialoguekit.nlg.nlg import NLG


ANNOTATED_DIALOGUE_FILE = "tests/data/annotated_dialogues.json"


# nlg class shared across tests.
@pytest.fixture
def nlg_class():
    nlg = NLG()
    nlg.template_from_file(ANNOTATED_DIALOGUE_FILE)
    return nlg


def test_generate_utterance_text(nlg_class):
    # A corner case where only one template found, i.e., REVEAL.EXPAND only has
    # something like the {TITLE}.
    expected_response1 = AnnotatedUtterance(
        text="something like the A Test Movie Title",
        intent=Intent("REVEAL.EXPAND"),
    )
    expected_response1.add_annotation(
        Annotation(slot="TITLE", value="A Test Movie Title")
    )
    sample_response_text = [
        (
            Intent("REVEAL.EXPAND"),
            [Annotation(slot="TITLE", value="A Test Movie Title")],
            expected_response1,
        )
    ]
    for intent, slot_values, expected_response in sample_response_text:
        generated_response = nlg_class.generate_utterance_text(
            intent, slot_values
        )
        assert generated_response == expected_response


def test_none_annotations(nlg_class):
    test = nlg_class.generate_utterance_text(Intent("COMPLETE"), None)

    assert test.intent == Intent("COMPLETE")
