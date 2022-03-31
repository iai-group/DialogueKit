"""Natural language understanding."""

from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance


class NLU:
    """Represents a Natural Language Understanding (NLU) component."""

    def __init__(self, intent_classifier, slot_annotators) -> None:
        """Initializes the NLU component."""
        self.__intent_classifier = intent_classifier
        self.__slot_annotators = slot_annotators

    def get_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of a given agent utterance."""
        return self.__intent_classifier.get_intent(utterance)

    def annotate_slot_values(self, utterance: Utterance) -> None:
        """Annotates a given utterance."""
        for slot_annotator in self.__slot_annotators:
            for annotation in slot_annotator.get_annotations(utterance):
                utterance.add_annotation(annotation)
