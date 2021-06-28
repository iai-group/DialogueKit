"""Interface representing the basic unit of communication."""

from enum import Enum
from typing import List

from dialoguekit.core.annotation import Annotation


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
        self.__text = text
        self.__utterance_type = utterance_type
        self.__annotations = []

    @property
    def text(self) -> str:
        return self.__text

    @property
    def utterance_type(self) -> UtteranceType:
        return self.__utterance_type

    def add_annotation(self, annotation) -> None:
        """Adds an annotation to the utterance.

        Args:
            annotation: Annotation instance.
        """
        self.__annotations.append(annotation)

    def get_annotations(self) -> List[Annotation]:
        """Returns the available annotations for the utterance.

        Return: List of Annotation instances.
        """
        return self.__annotations

    def get_text_placeholders(self) -> str:
        """Returns the utterance text with annotations replaces with
        placeholders."""
        # TODO
        return ""
