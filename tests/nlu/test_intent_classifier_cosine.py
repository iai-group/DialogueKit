"""Tests for intent classifier cosine."""
import pytest
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.intent_classifier_cosine import IntentClassifierCosine

PLACEHOLDER = "(.*)"


# Utterance intent mappings for finding exact the same patterns.
@pytest.fixture
def utterance_intent_mappings_1():
    mappings_1 = {
        f"You should try {PLACEHOLDER}!": Intent("intent 1"),
        f"There's also {PLACEHOLDER}!": Intent("intent 2"),
        f"Also check out {PLACEHOLDER}!": Intent("intent 3"),
        f"I found {PLACEHOLDER} for you!": Intent("intent 4"),
        f"I also found {PLACEHOLDER}!": Intent("intent 5"),
        f"I think you should give {PLACEHOLDER} a shot!": Intent("intent 6"),
    }
    return mappings_1


# Utterance intent mappings for finding similar patterns.
@pytest.fixture
def utterance_intent_mappings_2():
    mappings_2 = {
        f"You should give {PLACEHOLDER} a try!": Intent("intent 1"),
        f"You might want to check {PLACEHOLDER}": Intent("intent 3"),
    }
    return mappings_2


def test_get_intent_exact_patterns(utterance_intent_mappings_1):
    intent_classifier = IntentClassifierCosine(utterance_intent_mappings_1)
    for utterance_template, intent in utterance_intent_mappings_1.items():
        utterance_text = utterance_template.replace(PLACEHOLDER, "RANDOM_ITEM")
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label


def test_get_intent_similar_patterns(
    utterance_intent_mappings_1, utterance_intent_mappings_2
):
    intent_classifier = IntentClassifierCosine(utterance_intent_mappings_1)
    for utterance_template, intent in utterance_intent_mappings_2.items():
        utterance_text = utterance_template.replace(PLACEHOLDER, "RANDOM_ITEM")
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label
