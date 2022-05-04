"""Interface representing the basic unit of communication."""


from typing import Text


class Utterance:
    """Represents an utterance."""

    def __init__(self, text: str) -> None:
        """Initializes an utterance.

        Args:
            text: Utterance text.
        """
        self._text = text

    def __str__(self) -> Text:
        return self._text

    def __repr__(self) -> Text:
        return f"Utterance({self._text})"

    def __hash__(self) -> int:
        return hash(self._text)

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
        if not isinstance(__o, Utterance):
            return False
        if self._text != __o._text:
            return False

        return True

    @property
    def text(self) -> str:
        return self._text
