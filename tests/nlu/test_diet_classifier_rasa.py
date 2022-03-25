"""Tests for IntentClassifierRasa."""

import pytest
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.models.diet_classifier_rasa import IntentClassifierRasa

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
        ]
    ]


@pytest.fixture
def labels_1():
    return [Intent(f"intent {i}") for i in range(1, 6)]


@pytest.fixture
def utterances_2():
    return [
        Utterance(text)
        for text in [
            f"You should give {PLACEHOLDER} a try!",
            f"You might want to check out {PLACEHOLDER}",
        ]
    ]


@pytest.fixture
def labels_2():
    return [Intent(f"intent {i}") for i in [1, 3]]


def test_get_intent_exact_patterns(intents, utterances_1, labels_1):
    intent_classifier = IntentClassifierRasa(intents)
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
    intent_classifier = IntentClassifierRasa(intents)
    intent_classifier.train_model(utterances_1, labels_1)
    for utterance_template, intent in zip(utterances_2, labels_2):
        utterance_text = utterance_template.text.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label
