"""Test for intent classifier cosine"""

import unittest
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.intent_classifier_cosine import IntentClassifierCosine

PLACEHOLDER = "(.*)"


class TestIntentClassifierCosine(unittest.TestCase):
    def test_get_intent(self):
        # Given
        utterance_intent_mapping = {
            f"You should try {PLACEHOLDER}!": Intent("intent 1"),
            f"There's also {PLACEHOLDER}!": Intent("intent 2"),
            f"Also check out {PLACEHOLDER}!": Intent("intent 3"),
            f"I found {PLACEHOLDER} for you!": Intent("intent 4"),
            f"I also found {PLACEHOLDER}!": Intent("intent 5"),
            f"I think you should give {PLACEHOLDER} a shot!": Intent(
                "intent 6"
            ),
        }

        intent_classifier = IntentClassifierCosine(utterance_intent_mapping)

        # Then
        for utterance_template, intent in utterance_intent_mapping.items():
            utterance_text = utterance_template.replace(
                PLACEHOLDER, "RANDOM_ITEM"
            )
            utterance = Utterance(utterance_text)
            predicted_intent = intent_classifier.get_intent(utterance)
            self.assertEqual(predicted_intent.intent, intent.intent)
