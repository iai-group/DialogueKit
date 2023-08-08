"""Tests for IntentClassifierRasa."""

import os
from typing import List
from unittest import mock

import pytest
from rasa.nlu.classifiers.diet_classifier import DIETClassifier

from dialoguekit.core import Intent, Utterance
from dialoguekit.nlu import IntentClassifierRasa
from dialoguekit.participant import DialogueParticipant

PLACEHOLDER = "(.*)"


@pytest.fixture
def intents() -> List[Intent]:
    """List of intents fixture."""
    return [Intent(f"intent {i}") for i in range(1, 7)]


@pytest.fixture
def utterances_1() -> List[Utterance]:
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
def labels_1() -> List[Intent]:
    """List of intent labels fixture."""
    return [Intent(f"intent {i}") for i in range(1, 6)]


@pytest.fixture
def utterances_2() -> List[Utterance]:
    """List of utterances fixture."""
    return [
        Utterance(text, participant=DialogueParticipant.AGENT)
        for text in [
            f"You should give {PLACEHOLDER} a try!",
            f"You might want to check out {PLACEHOLDER}",
        ]
    ]


@pytest.fixture
def labels_2() -> List[Intent]:
    """List of intent labels fixture."""
    return [Intent(f"intent {i}") for i in [1, 3]]


def test_classify_intent_exact_patterns(
    intents: List[Intent],
    utterances_1: List[Utterance],
    labels_1: List[Intent],
) -> None:
    """Tests label prediction.

    Args:
        intents: Test intents
        utterances_1: Test utterances to train on
        labels_1: Test utterance intent labels.
    """
    intent_classifier = IntentClassifierRasa(intents, model_path="tests/.rasa")
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
    os.system("rm -rf tests/.rasa")


def test_classify_intent_similar_patterns(
    intents: List[Intent],
    utterances_1: List[Utterance],
    labels_1: List[Intent],
    utterances_2: List[Utterance],
    labels_2: List[Intent],
) -> None:
    """Tests label prediction.

    Args:
        intents: Test intents.
        utterances_1: Test utterances.
        labels_1: Test labels.
        utterances_2: Secondary test utterances.
        labels_2: Secondary test labels.
    """
    intent_classifier = IntentClassifierRasa(intents, model_path="tests/.rasa")
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
    os.system("rm -rf tests/.rasa")


def test_load_save_model(
    intents: List[Intent], utterances_1: List[Utterance], labels_1: List[Intent]
) -> None:
    """Tests loading and saving model."""
    intent_classifier = IntentClassifierRasa(intents, model_path="tests/.rasa")
    intent_classifier.train_model(utterances_1, labels_1)
    intent_classifier.save_model()

    assert os.path.exists("tests/.rasa/pipeline.pkl")

    intent_classifer_2 = IntentClassifierRasa(intents, model_path="tests/.rasa")

    assert len(intent_classifer_2._component_pipeline) == len(
        intent_classifier._component_pipeline
    )
    assert isinstance(intent_classifer_2._diet, DIETClassifier)
    assert intent_classifer_2._processes_utterances == {}
    os.system("rm -rf tests/.rasa")


@mock.patch.object(IntentClassifierRasa, "init_pipeline")
def test_load_empty_model(
    mock_init_pipeline: mock.MagicMock, intents: List[Intent]
) -> None:
    """Tests if pipeline is initialized when loading empty model."""
    _ = IntentClassifierRasa(intents, model_path="tests/.rasa")
    mock_init_pipeline.assert_called_once()
    os.system("rm -rf tests/.rasa")
