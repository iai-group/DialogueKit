"""Interface representing an intent."""


class Intent:
    """Represents an intent."""

    def __init__(self, label: str) -> None:
        """Initializes the intent.

        Args:
            Label: intent label.
        """
        self.__label = label

    @property
    def label(self) -> str:
        return self.__label
