"""Dialogue act extractor with disjoint intent classification and slot filling.

It is assumed that the intent classifier assigns a single intent to the
utterance that corresponds to the slot-value pairs extracted by the slot-value
annotators.
"""

from __future__ import annotations

import os
from typing import List, cast

from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.intent import Intent
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlu.dialogue_acts_extractor import DialogueActsExtractor
from dialoguekit.nlu.intent_classifier import IntentClassifier
from dialoguekit.nlu.slot_value_annotator import SlotValueAnnotator


class DisjointDialogueActExtractor(DialogueActsExtractor):
    def __init__(
        self,
        intent_classifier: IntentClassifier,
        slot_value_annotators: List[SlotValueAnnotator],
    ) -> None:
        """Initializes the dialogue act extractor.

        Args:
            intent_classifier: Intent classifier.
            slot_value_annotators: List of slot-value annotators.
        """
        super().__init__()
        self._intent_classifier = intent_classifier
        self._slot_value_annotators = slot_value_annotators

    def classify_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of a given agent utterance."""
        return self._intent_classifier.classify_intent(utterance)

    def annotate_slot_values(
        self, utterance: Utterance
    ) -> List[SlotValueAnnotation]:
        """Annotates a given utterance with slot-value annotators.

        Args:
            utterance: Utterance to annotate.

        Returns:
            List of annotations.
        """
        annotation_list = []
        for slot_annotator in self._slot_value_annotators:
            annotation_list.extend(slot_annotator.get_annotations(utterance))
        return annotation_list

    def extract_dialogue_acts(self, utterance: Utterance) -> List[DialogueAct]:
        """Extracts a single dialogue act from an utterance.

        Args:
            utterance: Utterance.

        Returns:
            List with one dialogue act.
        """
        intent = self.classify_intent(utterance)
        annotations = self.annotate_slot_values(utterance)
        if intent is None:
            return []
        return [DialogueAct(intent, annotations)]

    def save(self, path: str) -> None:
        """Saves the intent classifier and slot-value annotators to a folder.

        Args:
            path: Path to save the dialogue act extractor.
        """
        if not os.path.exists(path):
            os.makedirs(path)

        intent_classifier_path = os.path.join(path, "intent_classifier")
        self._intent_classifier.save_model(intent_classifier_path)

        for i, slot_value_annotator in enumerate(self._slot_value_annotators):
            slot_value_annotator_path = os.path.join(
                path, f"slot_value_annotator_{i}"
            )
            slot_value_annotator.save_annotator(slot_value_annotator_path)

    @classmethod
    def load(self, path: str) -> DisjointDialogueActExtractor:
        """Loads the intent classifier and slot-value annotators from a folder.

        Args:
            path: Path to folder with intent classifier and slot-value
              annotators.

        Raises:
            FileNotFoundError: If the given folder does not exist.

        Returns:
            Dialogue act extractor with loaded models.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Folder {path} does not exist")

        intent_classifier_path = os.path.join(path, "intent_classifier")
        intent_classifier = IntentClassifier.load_model(intent_classifier_path)

        slot_value_annotators = []
        for _, slot_value_annotator_filename in enumerate(
            filter(lambda x: "slot_value_annotator" in x, os.listdir(path))
        ):
            slot_value_annotator = SlotValueAnnotator.load_annotator(
                os.path.join(path, slot_value_annotator_filename)
            )
            slot_value_annotators.append(
                cast(SlotValueAnnotator, slot_value_annotator)
            )

        return DisjointDialogueActExtractor(
            intent_classifier, slot_value_annotators
        )
