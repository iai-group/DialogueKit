"""Natural language understanding."""

from typing import List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlu.annotator import Annotator
from dialoguekit.nlu.dialogue_acts_extractor import DialogueActsExtractor


class NLU:
    def __init__(
        self,
        dialogue_act_extractor: DialogueActsExtractor,
        annotators: List[Annotator] = None,
    ) -> None:
        """Initializes the NLU module.

        Args:
            dialogue_act_extractor: Dialogue act extractor.
            annotators: List of annotators.
        """
        self._dialogue_act_extractor = dialogue_act_extractor
        self._annotators = annotators if annotators is not None else []

    def extract_dialogue_acts(self, utterance: Utterance) -> List[DialogueAct]:
        """Extracts dialogue acts from an utterance.

        Args:
            utterance: Utterance.

        Returns:
            List of dialogue acts.
        """
        return self._dialogue_act_extractor.extract_dialogue_acts(utterance)

    def get_annotations(self, utterance: Utterance) -> List[Annotation]:
        """Annotates an utterance.

        Args:
            utterance: Utterance.

        Returns:
            List of annotations.
        """
        annotation_list = []
        for annotator in self._annotators:
            annotation_list.extend(annotator.get_annotations(utterance))
        return annotation_list
