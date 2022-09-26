"""Tests for IntentClassifierCosine."""

import os

import pytest
from dialoguekit.core import Intent, Utterance
from dialoguekit.nlu import IntentClassifierCosine
from dialoguekit.participant import DialogueParticipant

PLACEHOLDER = "(.*)"


@pytest.fixture
def intents():
    """Testing intents fixture."""
    return [Intent(f"intent {i}") for i in range(1, 7)]


@pytest.fixture
def utterances_1():
    """Testing utterances fixture."""
    return [
        Utterance(text, participant=DialogueParticipant.AGENT)
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
    """Testing label fixture."""
    return [Intent(f"intent {i}") for i in range(1, 7)]


@pytest.fixture
def utterances_2():
    """Testing utterances fixture."""
    return [
        Utterance(text, participant=DialogueParticipant.AGENT)
        for text in [
            f"You should give {PLACEHOLDER} a try!",
            f"You might want to check {PLACEHOLDER}",
        ]
    ]


@pytest.fixture
def labels_2():
    """Testing label fixture."""
    return [Intent(f"intent {i}") for i in [1, 3]]


def test_classify_intent_exact_patterns(intents, utterances_1, labels_1):
    """Tests get label.

    Args:
        intents: Testing intents.
        utterances_1: Testing utterances.
        labels_1: Testing labels.
    """
    intent_classifier = IntentClassifierCosine(intents)
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
    """Tests get similar intent.

    Args:
        intents: Testing intents.
        utterances_1: Testing utterances.
        labels_1: Testing labels.
        utterances_2: Secondary utterances.
        labels_2: Secondary labels.
    """
    intent_classifier = IntentClassifierCosine(intents)
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


def test_save_and_load_model(tmp_path, intents, utterances_1, labels_1):
    """Tests saving and loading of model.

    Args:
        tmp_path: Pytest tmp_path.
        intents: Testing intents.
        utterances_1: Testing utterances.
        labels_1: Testing labels.
    """
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
        utterance = Utterance(
            utterance_text, participant=DialogueParticipant.AGENT
        )
        predicted_intent = intent_classifier.classify_intent(utterance)
        assert predicted_intent.label == intent.label
