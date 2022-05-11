"""Tests for IntentClassifierCosine."""

import pytest
import os
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.models.intent_classifier_cosine import (
    IntentClassifierCosine,
)

PLACEHOLDER = "(.*)"


@pytest.fixture
def intents():
    return [Intent(f"intent {i}") for i in range(1, 7)]


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


@pytest.fixture
def utterances_2():
    return [
        Utterance(text)
        for text in [
            f"You should give {PLACEHOLDER} a try!",
            f"You might want to check {PLACEHOLDER}",
        ]
    ]


@pytest.fixture
def labels_2():
    return [Intent(f"intent {i}") for i in [1, 3]]


def test_get_intent_exact_patterns(intents, utterances_1, labels_1):
    intent_classifier = IntentClassifierCosine(intents)
    intent_classifier.train_model(utterances_1, labels_1)
    for utterance_template, intent in zip(utterances_1, labels_1):
        utterance_text = utterance_template.text.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label


def test_get_intent_similar_patterns(
    intents, utterances_1, labels_1, utterances_2, labels_2
):
    intent_classifier = IntentClassifierCosine(intents)
    intent_classifier.train_model(utterances_1, labels_1)
    for utterance_template, intent in zip(utterances_2, labels_2):
        utterance_text = utterance_template.text.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label


def test_save_and_load_model(tmp_path, intents, utterances_1, labels_1):
    save_to_dir = tmp_path
    full_path = save_to_dir.absolute()
    my_path = full_path.as_posix()

    intent_classifier = IntentClassifierCosine(intents)
    intent_classifier.train_model(utterances_1, labels_1)
    intent_classifier.save_model(file_path=os.path.join(my_path, ""))

    intent_classifier = None
    intent_classifier = IntentClassifierCosine(intents)
    intent_classifier.load_model(file_path=os.path.join(my_path, ""))

    for utterance_template, intent in zip(utterances_1, labels_1):
        utterance_text = utterance_template.text.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label
