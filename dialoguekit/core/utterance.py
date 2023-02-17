"""Interface representing the basic unit of communication."""

from dataclasses import dataclass, field
from datetime import datetime

from dialoguekit.participant.participant import DialogueParticipant


@dataclass(eq=True, unsafe_hash=True)
class Utterance:
    """Represents an utterance."""

    text: str = field(hash=True)
    participant: DialogueParticipant = field(hash=True)
    timestamp: datetime = field(default=None, hash=True)

    def _timestamp_text(self) -> str:
        """Returns the timestamp as a string.

        If no timestamp, this method will return an empty string.

        Returns:
            Timestamp with the format: `%m/%d/%Y, %H:%M:%S`.
        """
        if self.timestamp:
            return self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        return ""
