"""Interface representing the basic unit of communication."""

from enum import Enum


class UtteranceType(Enum):
    """Represents different types of utterances."""

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

    @property
    def text(self):
        return self._text

    @property
    def utterance_type(self):
        return self._utterance_type
