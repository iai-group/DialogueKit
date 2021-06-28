"""Test for intent classifier cosine"""

import pytest
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.intent_classifier_cosine import IntentClassifierCosine

PLACEHOLDER = "(.*)"


def test_get_intent():
    # Given
    utterance_intent_mapping = {
        f"You should try {PLACEHOLDER}!": Intent("intent 1"),
        f"There's also {PLACEHOLDER}!": Intent("intent 2"),
        f"Also check out {PLACEHOLDER}!": Intent("intent 3"),
        f"I found {PLACEHOLDER} for you!": Intent("intent 4"),
        f"I also found {PLACEHOLDER}!": Intent("intent 5"),
        f"I think you should give {PLACEHOLDER} a shot!": Intent(
            "intent 6"
        )
    }

    intent_classifier = IntentClassifierCosine(utterance_intent_mapping)

    # Then
    for utterance_template, intent in utterance_intent_mapping.items():
        utterance_text = utterance_template.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label

    # Given that when there is no exact match, but some of the key words
    extra_utterance_intent_mappings = {
        f"You should give {PLACEHOLDER} a try!": Intent("intent 1"),
        f"You might want to check {PLACEHOLDER}": Intent("intent 3"),
    }

    # Then
    for utterance_template, intent in extra_utterance_intent_mappings.items():
        utterance_text = utterance_template.replace(
            PLACEHOLDER, "RANDOM_ITEM"
        )
        utterance = Utterance(utterance_text)
        predicted_intent = intent_classifier.get_intent(utterance)
        assert predicted_intent.label == intent.label
