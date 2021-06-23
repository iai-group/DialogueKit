"""Interface representing the basic unit of communication."""

from enum import Enum


class UtteranceType(Enum):
    """Represents different types of utterances."""

    # TODO: These should be replaced with intents.
    MESSAGE = 0
    WELCOME = 1
    EXIT = 2


class Utterance:
    """Represents a utterance."""

    def __init__(
        self, text: str, utterance_type: UtteranceType = UtteranceType.MESSAGE
    ) -> None:
        """Initializes an utterance.

        Args:
            text: Utterance text.
            utterance_type: Utterance type (default: MESSAGE).
        """
        self._text = text
        self._utterance_type = utterance_type
        self._annotations = []

    @property
    def text(self) -> str:
        return self._text

    @property
    def utterance_type(self) -> UtteranceType:
        return self._utterance_type

    def add_annotation(self, annotation) -> None:
        """Adds an annotation to the utterance.

        Args:
            annotation: Annotation instance.
        """
        self._annotations.append(annotation)

    def get_text_placeholders(self) -> str:
        """Returns the utterance text with annotations replaces with
        placeholders."""
        # TODO
        return ""
