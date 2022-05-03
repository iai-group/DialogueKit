"""Interface representing the basic unit of communication."""

from typing import List, Optional, Text

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance


class AnnotatedUtterance(Utterance):
    """Represents an utterance, with additional info."""

    def __init__(self, text: str, intent: Optional[Intent] = None) -> None:
        """Initializes an AnnotatedUtterance.

        The AnnotatedUtterance is a Utterance with additional information.
        In some cases we want to send an utterance with the Intent and or
        Annotations.

        Args:
            text: Utterance text.
            intent: The intent of the utterance.
        """

        super().__init__(text=text)
        self._intent = intent
        self._annotations = []

    def __str__(self) -> Text:
        return self._text

    def __repr__(self) -> Text:
        return f"AnnotatedUtterance({self._text})"

    def __hash__(self) -> int:
        hashed_annotations = "".join(
            [str(hash(annotation)) for annotation in self._annotations]
        )
        return hash((self._text, self._intent, hashed_annotations))

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
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

    @property
    def utterance(self) -> Utterance:
        return Utterance(self.text)

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
