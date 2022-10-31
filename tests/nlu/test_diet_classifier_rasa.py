"""Tests for IntentClassifierRasa."""

import pytest
from dialoguekit.core import Intent, Utterance
from dialoguekit.nlu import IntentClassifierRasa
from dialoguekit.participant import DialogueParticipant

PLACEHOLDER = "(.*)"


@pytest.fixture
def intents():
    """List of intents fixture."""
    return [Intent(f"intent {i}") for i in range(1, 7)]


@pytest.fixture
def utterances_1():
    """List of utterances fixture."""
    return [
        Utterance(text, participant=DialogueParticipant.AGENT)
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
    """List of intent labels fixture."""
    return [Intent(f"intent {i}") for i in range(1, 6)]


@pytest.fixture
def utterances_2():
    """List of utterances fixture."""
    return [
        Utterance(text, participant=DialogueParticipant.AGENT)
        for text in [
            f"You should give {PLACEHOLDER} a try!",
            f"You might want to check out {PLACEHOLDER}",
        ]
    ]


@pytest.fixture
def labels_2():
    """List of intent labels fixture."""
    return [Intent(f"intent {i}") for i in [1, 3]]


def test_classify_intent_exact_patterns(intents, utterances_1, labels_1):
    """Tests label prediction.

    Args:
        intents: Test intents
        utterances_1: Test utterances to train on
        labels_1: Test utterance intent labels.
    """
    intent_classifier = IntentClassifierRasa(intents)
    intent_classifier.train_model(utterances_1, labels_1)
    for utterance_template, intent in zip(utterances_1, labels_1):
        utterance_text = utterance_template.text.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(
            utterance_text, participant=DialogueParticipant.AGENT
        )
        predicted_intent = intent_classifier.classify_intent(utterance)
        assert predicted_intent.label == intent.label


def test_classify_intent_similar_patterns(
    intents, utterances_1, labels_1, utterances_2, labels_2
):
    """Tests label prediction.

    Args:
        intents: Test intents.
        utterances_1: Test utterances.
        labels_1: Test labels.
        utterances_2: Secondary test utterances.
        labels_2: Secondary test labels.
    """
    intent_classifier = IntentClassifierRasa(intents)
    intent_classifier.train_model(utterances_1, labels_1)
    for utterance_template, intent in zip(utterances_2, labels_2):
        utterance_text = utterance_template.text.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(
            utterance_text, participant=DialogueParticipant.AGENT
        )
        predicted_intent = intent_classifier.classify_intent(utterance)
        assert predicted_intent.label == intent.label
