"""Test cases for NLG."""

import json

import pytest

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.intent import Intent
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation
from dialoguekit.nlg.nlg_template import TemplateNLG
from dialoguekit.nlg.template_from_training_data import (
    extract_utterance_template,
)
from dialoguekit.participant.participant import DialogueParticipant

ANNOTATED_DIALOGUE_FILE = "tests/data/annotated_dialogues.json"


# NLG class shared across tests.
@pytest.fixture
def nlg_class() -> TemplateNLG:
    """Template MLG fixture."""
    template = extract_utterance_template(
        annotated_dialogue_file=ANNOTATED_DIALOGUE_FILE,
    )
    nlg = TemplateNLG(response_templates=template)
    return nlg


def test_generate_utterance_text(nlg_class: TemplateNLG):
    """Tests utterance generation."""
    expected_response1 = AnnotatedUtterance(
        text="something like the A Test Movie Title",
        dialogue_acts=[
            DialogueAct(
                intent=Intent("REVEAL.EXPAND"),
                annotations=[
                    SlotValueAnnotation(
                        slot="TITLE", value="A Test Movie Title"
                    )
                ],
            )
        ],
        participant=DialogueParticipant.AGENT,
    )

    sample_response_text = [
        (
            [
                DialogueAct(
                    intent=Intent("REVEAL.EXPAND"),
                    annotations=[
                        SlotValueAnnotation(
                            slot="TITLE", value="A Test Movie Title"
                        )
                    ],
                )
            ],
            expected_response1,
        )
    ]
    for dialogue_acts, expected_response in sample_response_text:
        generated_response = nlg_class.generate_utterance_text(
            dialogue_acts=dialogue_acts
        )
        assert generated_response == expected_response

    generated_response = nlg_class.generate_utterance_text(
        dialogue_acts=[DialogueAct(intent=Intent("NOT_AN_INTENT"))]
    )
    assert generated_response.text == "Sorry, I did not understand you."
    assert generated_response.get_intents() == [Intent("NOT_AN_INTENT")]


def test_generate_utterance_text_force_annotation(nlg_class: TemplateNLG):
    """Tests utterance generation with forcing annotations."""
    test = nlg_class.generate_utterance_text(
        dialogue_acts=[DialogueAct(intent=Intent("COMPLETE"))],
        force_annotation=True,
    )
    assert test.get_intents() == [Intent("COMPLETE")]

    test = nlg_class.generate_utterance_text(
        dialogue_acts=[
            DialogueAct(
                intent=Intent("TRAVERSE.REPEAT"),
                annotations=[
                    SlotValueAnnotation(
                        slot="DIRECTOR", value="TEST_DIRECTOR_NAME"
                    )
                ],
            )
        ],
        force_annotation=True,
    )
    assert test.text == "TEST_DIRECTOR_NAME name"


def test_no_annotations(nlg_class: TemplateNLG):
    """Tests utterance generation without annotations."""
    test = nlg_class.generate_utterance_text(
        dialogue_acts=[DialogueAct(intent=Intent("COMPLETE"))]
    )

    assert test.get_intents() == [Intent("COMPLETE")]


def test_filter_templates(nlg_class: TemplateNLG):
    """Tests utterance generation with filtering."""
    test_response = nlg_class.generate_utterance_text(
        dialogue_acts=[
            DialogueAct(
                intent=Intent("REVEAL.EXPAND"),
                annotations=[
                    SlotValueAnnotation(slot="TITLE", value="test_movie_title")
                ],
            )
        ],
    )

    assert test_response
    assert test_response.text == "something like the test_movie_title"

    with pytest.raises(ValueError):
        test_response = nlg_class.generate_utterance_text(
            dialogue_acts=[DialogueAct(intent=Intent("REVEAL.EXPAND"))]
        )


def test_get_intent_annotation_specifications(nlg_class: TemplateNLG):
    """Tests intent annotations specifications getter."""
    test_response = nlg_class.get_intent_annotation_specifications(
        dialogue_acts=[DialogueAct(intent=Intent("REVEAL.REFINE"))]
    )
    assert test_response

    with pytest.raises(TypeError):
        nlg_class.get_intent_annotation_specifications(
            dialogue_acts=[DialogueAct(intent=Intent("NOT_AN_INTENT"))]
        )


def test_dump_templates(nlg_class: TemplateNLG, tmp_path):
    """Tests template export."""
    save_to_dir = tmp_path
    full_path = save_to_dir.absolute()
    my_path = full_path.as_posix()

    nlg_class.dump_template(filepath=f"{my_path}/nlg_dump.json")

    with open(f"{my_path}/nlg_dump.json", "r", encoding="utf-8") as file:
        json_template = json.load(file)
        assert len(json_template.keys()) == len(
            nlg_class._response_templates.keys()
        )

        for intents in json_template.keys():
            assert intents in nlg_class._response_templates.keys()
