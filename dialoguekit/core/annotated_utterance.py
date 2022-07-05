"""Interface extending utterances with annotations."""

from typing import List, Dict, Any, Optional, Union
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance


class AnnotatedUtterance(Utterance):
    """Represents an utterance, with additional info."""

    def __init__(
        self,
        text: str,
        intent: Optional[Intent] = None,
        annotations: Optional[List[Annotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initializes an AnnotatedUtterance.

        The AnnotatedUtterance is a Utterance with additional information.
        In some cases we want to send an utterance with the Intent and or
        Annotations.

        Args:
            text: Utterance text.
            intent: The intent of the utterance.
            annotations: Annotations of the Utterance text.
            metadata: Dict with optional attributes (satisfaction etc.).
        """

        super().__init__(text=text)
        self._intent = intent
        self._annotations = []
        if annotations:
            self._annotations.extend(annotations)
        self._metadata = metadata if metadata else {}

    def __str__(self) -> str:
        return self._text

    def __repr__(self) -> str:
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

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def add_annotation(
        self, annotation: Union[Annotation, List[Annotation]]
    ) -> None:
        """Adds an annotation to the utterance.

        Args:
            annotation: Annotation instance.
        """
        if isinstance(annotation, List):
            self._annotations.extend(annotation)
        elif isinstance(annotation, Annotation):
            self._annotations.append(annotation)
        else:
            raise TypeError(
                "Provided annotation is not of type Annotation or \
                    List[Annotation]"
            )

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
