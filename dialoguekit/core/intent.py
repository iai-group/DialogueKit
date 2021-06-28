"""Interface representing an intent."""


class Intent:
    """Represents an intent."""

    def __init__(self, label: str) -> None:
        """Initializes the intent.

        Args:
            label: intent label
        """
        self.__label = label

    @property
    def label(self) -> str:
        return self.__label
