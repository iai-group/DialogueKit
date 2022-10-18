"""Interface representing the basic unit of communication."""

from datetime import datetime
from typing import Optional, Text

from dialoguekit.participant.participant import DialogueParticipant


class Utterance:
    def __init__(
        self,
        text: str,
        participant: DialogueParticipant,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Represents an utterance.

        Args:
            text: Utterance text.
            participant: Who said the utterance.
            timestamp: When was the utterance uttered.
        """
        self._text = text
        self._participant = participant
        self._timestamp = timestamp

    def __str__(self) -> Text:
        """Returns the utterance text."""
        return self._text

    def __repr__(self) -> Text:
        """Represents the utterance as a string."""
        if self._timestamp:
            time = self._timestamp.strftime("%m/%d/%Y, %H:%M:%S")
            return f"Utterance({self._text}, {self._participant.value}, {time})"
        return f"Utterance({self._text}, {self._participant.value})"

    def __hash__(self) -> int:
        """Represents the utterance as a hash."""
        return hash(f"{self._text}{self._participant}{self._timestamp_text()}")

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
        if not isinstance(__o, Utterance):
            return False
        if self._text != __o._text:
            return False
        if self._timestamp != __o._timestamp:
            return False
        if self._participant != __o._participant:
            return False
        return True

    @property
    def text(self) -> str:
        """Returns the utterance text."""
        return self._text

    @property
    def participant(self) -> DialogueParticipant:
        """Returns the utterance participant."""
        return self._participant

    @property
    def timestamp(self) -> datetime:
        """Returns the utterance timestamp."""
        return self._timestamp

    def _timestamp_text(self) -> str:
        """Returns the timestamp as a string.

        If no timestamp, this method will return an empty string.

        Returns:
            Timestamp with the format: `%m/%d/%Y, %H:%M:%S`.
        """
        if self._timestamp:
            return self._timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        return ""
