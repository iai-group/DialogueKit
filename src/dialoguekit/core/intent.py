"""Interface representing an intent."""


class Intent:
    def __init__(self, label: str) -> None:
        """Initializes the intent.

        Args:
            label: Intent label.
        """
        self._label = label

    def __str__(self) -> str:
        return self._label

    @property
    def label(self) -> str:
        return self._label
