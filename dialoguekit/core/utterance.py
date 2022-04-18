"""Interface representing the basic unit of communication."""


class Utterance:
    """Represents an utterance."""

    def __init__(self, text: str) -> None:
        """Initializes an utterance.

        Args:
            text: Utterance text.
        """
        self._text = text

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

    def __str__(self) -> str:
        return self._text
