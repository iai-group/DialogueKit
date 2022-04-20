"""Interface representing an intent."""


from typing import Text


class Intent:
    def __init__(self, label: str) -> None:
        """Initializes the intent.

        Args:
            label: Intent label.
        """
        self._label = label

    def __str__(self) -> Text:
        return self._label

    def __repr__(self) -> Text:
        return f"Intent({self._label})"

    def __hash__(self) -> int:
        return hash(self._label)

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
        if not isinstance(__o, Intent):
            return False
        if self._label != __o._label:
            return False
        return True

    @property
    def label(self) -> str:
        return self._label
