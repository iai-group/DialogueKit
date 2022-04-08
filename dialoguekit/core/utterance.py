"""Interface representing the basic unit of communication."""


class Utterance:
    """Represents an utterance."""

    def __init__(self, text: str) -> None:
        """Initializes an utterance.

        Args:
            text: Utterance text.
        """
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    def __str__(self) -> str:
        return self._text
