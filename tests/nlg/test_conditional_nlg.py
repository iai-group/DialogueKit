"""Test cases for NLG."""

import json

import pytest

from dialoguekit.core import AnnotatedUtterance, Intent, SlotValueAnnotation
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.nlg import ConditionalNLG
from dialoguekit.nlg.template_from_training_data import (
    extract_utterance_template,
)
from dialoguekit.nlu import SatisfactionClassifierSVM
from dialoguekit.participant import DialogueParticipant

ANNOTATED_DIALOGUE_FILE = "tests/data/annotated_dialogues.json"


# NLG class shared across tests.
@pytest.fixture
def nlg_class() -> ConditionalNLG:
    """Tests class init.

    This method is also a testing fixture used for the rest of the tests.
    """
    template = extract_utterance_template(
        annotated_dialogue_file=ANNOTATED_DIALOGUE_FILE,
        satisfaction_classifier=SatisfactionClassifierSVM(),
    )
    nlg = ConditionalNLG(response_templates=template)
    return nlg


def test_generate_utterance_text(nlg_class: ConditionalNLG):
    """Tests generation of utterances.

    A corner case where only one template found, i.e., REVEAL.EXPAND only has
    something like the {TITLE}.

    Args:
        nlg_class: Test NLG object.
    """
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
        metadata={"satisfaction": 2},
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
        generated_response = nlg_class.generate_utterance_text(dialogue_acts)
        assert generated_response == expected_response

    generated_response = nlg_class.generate_utterance_text(
        [DialogueAct(intent=Intent("NOT_AN_INTENT"))]
    )
    assert generated_response.text == "Sorry, I did not understand you."
    assert generated_response.get_intents() == [Intent("NOT_AN_INTENT")]


def test_generate_utterance_text_force_annotation(nlg_class: ConditionalNLG):
    """Tests utterance generation with annotations.

    A corner case where only one template found, i.e., REVEAL.EXPAND only has
    something like the {TITLE}.

    Args:
        nlg_class: Test NLG object.
    """
    test = nlg_class.generate_utterance_text(
        [DialogueAct(Intent("COMPLETE"), annotations=None)],
        force_annotation=True,
    )
    assert test.get_intents() == [Intent("COMPLETE")]

    test = nlg_class.generate_utterance_text(
        dialogue_acts=[
            DialogueAct(
                Intent("TRAVERSE.REPEAT"),
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


def test_no_annotations(nlg_class: ConditionalNLG):
    """Tests utterance generation without annotations.

    Args:
        nlg_class: Test NLG object.
    """
    test = nlg_class.generate_utterance_text(
        [DialogueAct(Intent("COMPLETE"), None)]
    )

    assert test.get_intents() == [Intent("COMPLETE")]


def test_generate_utterance_text_with_satisfaction(nlg_class: ConditionalNLG):
    """Tests utterance generation with metadata.

    Args:
        nlg_class: Test NLG object.
    """
    test_response = nlg_class.generate_utterance_text_conditional(
        dialogue_acts=[DialogueAct(Intent("COMPLETE"))],
        conditional="satisfaction",
        conditional_value=3,
    )

    assert test_response.metadata.get("satisfaction") == 2


def test_filter_templates(nlg_class: ConditionalNLG):
    """Tests filtering of the template.

    Args:
        nlg_class: Test NLG object.
    """
    test_response = nlg_class.generate_utterance_text_conditional(
        dialogue_acts=[
            DialogueAct(
                intent=Intent("REVEAL.EXPAND"),
                annotations=[
                    SlotValueAnnotation(slot="TITLE", value="test_movie_title")
                ],
            )
        ],
        conditional="satisfaction",
        conditional_value=3,
    )

    assert test_response
    assert test_response.text == "something like the test_movie_title"

    with pytest.raises(ValueError):
        test_response = nlg_class.generate_utterance_text_conditional(
            [DialogueAct(intent=Intent("REVEAL.EXPAND"))],
            conditional="satisfaction",
            conditional_value=3,
        )


def test_get_intent_annotation_specifications(nlg_class: ConditionalNLG):
    """Tests annotation statistics method.

    Args:
        nlg_class: Test NLG object.
    """
    test_response = nlg_class.get_intent_annotation_specifications(
        [DialogueAct(intent=Intent("REVEAL.REFINE"))]
    )
    assert test_response

    with pytest.raises(TypeError):
        nlg_class.get_intent_annotation_specifications(
            [DialogueAct(intent=Intent("NOT_AN_INTENT"))]
        )


def test_dump_templates(nlg_class: ConditionalNLG, tmp_path):
    """Tests dumping of the template.

    Args:
        nlg_class: Test NLG object.
        tmp_path: Pytest tmp path.
    """
    save_to_dir = tmp_path
    full_path = save_to_dir.absolute()
    my_path = full_path.as_posix()

    nlg_class.dump_template(filepath=f"{my_path}/nlg_dump.json")

    with open(f"{my_path}/nlg_dump.json", "r", encoding="utf-8") as file:
        json_template = json.load(file)
        assert len(json_template.keys()) == len(
            nlg_class._response_templates.keys()
        )

        for intent in json_template.keys():
            assert intent in nlg_class._response_templates.keys()
