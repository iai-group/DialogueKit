"""Tests for AnnotationConverterRasa."""

import pytest
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.utils.annotation_converter_dialoguekit_to_rasa import (
    AnnotationConverterRasa,
)

PLACEHOLDER = "(.*)"


@pytest.fixture
def utterances_1():
    return [
        Utterance(text)
        for text in [
            f"You should try {PLACEHOLDER}!",
            f"There's also {PLACEHOLDER}!",
            f"Also check out {PLACEHOLDER}!",
            f"I found {PLACEHOLDER} for you!",
            f"I also found {PLACEHOLDER}!",
            f"I think you should give {PLACEHOLDER} a shot!",
        ]
    ]


@pytest.fixture
def labels_1():
    return [Intent(f"intent {i}") for i in range(1, 7)]


def test_read_original(tmp_path):
    save_to_dir = tmp_path
    # save_to_dir.mkdir()
    full_path = save_to_dir.absolute()
    my_path = full_path.as_posix()

    converter = AnnotationConverterRasa(
        filepath="tests/data/annotated_dialogues.json",
        save_to_path=my_path + "/",
    )
    converter.read_original()

    # Check slot value pairs
    assert len(converter._slot_value_pairs.keys()) == 5
    assert len(list(converter._slot_value_pairs.values())[0]) == 16

    # Check intent examples
    assert len(converter._intent_examples.keys()) == 2
    assert "USER" in converter._intent_examples.keys()
    assert "AGENT" in converter._intent_examples.keys()
    assert len(converter._intent_examples["USER"].keys()) == 10
    assert len(converter._intent_examples["AGENT"].keys()) == 9


def test_run(tmp_path):
    save_to_dir = tmp_path
    full_path = save_to_dir.absolute()
    my_path = full_path.as_posix()

    converter = AnnotationConverterRasa(
        filepath="tests/data/annotated_dialogues.json",
        save_to_path=my_path + "/",
    )

    converter.read_original()
    converter.run()

    p = save_to_dir.glob("**/*")
    files = [x for x in p if x.is_file()]

    # Check amount of docs
    assert len(files) == 4
    # TODO validate generated yml files.
    # https://github.com/iai-group/dialoguekit/issues/57


def test_dialoguekit_to_rasa(tmp_path, utterances_1, labels_1):
    save_to_dir = tmp_path
    full_path = save_to_dir.absolute()
    my_path = full_path.as_posix()

    converter = AnnotationConverterRasa(
        filepath="tests/data/annotated_dialogues.json",
        save_to_path=my_path + "/",
    )
    converter.dialoguekit_to_rasa(intents=labels_1, utterances=utterances_1)
