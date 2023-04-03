"""Natural language understanding."""

from typing import List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlu.intent_classifier import IntentClassifier
from dialoguekit.nlu.slot_annotator import SlotAnnotator


class NLU:
    def __init__(
        self,
        intent_classifier: IntentClassifier,
        slot_annotators: List[SlotAnnotator],
    ) -> None:
        """Represents a Natural Language Understanding (NLU) component.

        Args:
            intent_classifier: Intent classifier.
            slot_annotators: List of slot annotators.
        """
        self._intent_classifier = intent_classifier
        self._slot_annotators = slot_annotators

    def classify_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of a given agent utterance."""
        return self._intent_classifier.classify_intent(utterance)

    def annotate_slot_values(self, utterance: Utterance) -> List[Annotation]:
        """Annotates a given utterance with slot annotators.

        Args:
            utterance: Utterance to annotate.

        Returns:
            List of annotations.
        """
        annotation_list = []
        for slot_annotator in self._slot_annotators:
            annotation_list.extend(slot_annotator.get_annotations(utterance))
        return annotation_list
