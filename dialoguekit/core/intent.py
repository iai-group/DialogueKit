"""Interface representing an intent."""


class Intent:
    """Represents an intent."""

    def __init__(self, intent: str) -> None:
        """Initializes the intent."""
        self._intent = intent

    @property
    def intent(self):
        return self._intent
