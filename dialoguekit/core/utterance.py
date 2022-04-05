"""Interface representing the basic unit of communication."""

from typing import List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent


class Utterance:
    """Represents a utterance."""

    def __init__(self, text: str, intent: Intent = None) -> None:
        """Initializes an utterance.

        Args:
            text: Utterance text.
            utterance_type: Utterance type (default: MESSAGE).
        """
        self._text = text
        self._intent = intent
        self._annotations = []

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Utterance):
            return False
        if self._text != __o._text:
            return False
        if self._intent != __o._intent:
            return False

        if len(self._annotations) != len(__o._annotations):
            return False

        for annotation in self._annotations:
            if annotation not in __o._annotations:
                return False

        return True

    @property
    def text(self) -> str:
        return self._text

    @property
    def intent(self) -> Intent:
        return self._intent

    def __str__(self) -> str:
        return self._text

    def add_annotation(self, annotation) -> None:
        """Adds an annotation to the utterance.

        Args:
            annotation: Annotation instance.
        """
        self._annotations.append(annotation)

    def get_annotations(self) -> List[Annotation]:
        """Returns the available annotations for the utterance.

        Return: List of Annotation instances.
        """
        return self._annotations

    def get_text_placeholders(self) -> str:
        """Returns the utterance text with annotations replaced with
        placeholders."""
        # TODO See: https://github.com/iai-group/dialoguekit/issues/35
        return ""
