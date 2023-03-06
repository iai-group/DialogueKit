"""Interface representing the basic unit of communication."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from dialoguekit.participant.participant import DialogueParticipant


class Feedback(Enum):
    """Represents user's feedback."""

    NEGATIVE = 0
    POSITIVE = 1


@dataclass(eq=True, unsafe_hash=True)
class Utterance:
    """Represents an utterance."""

    text: str = field(hash=True)
    participant: DialogueParticipant = field(hash=True)
    timestamp: datetime = field(default=None, hash=True)
    feedback: Feedback = field(default=None, hash=True)

    def _timestamp_text(self) -> str:
        """Returns the timestamp as a string.

        If no timestamp, this method will return an empty string.

        Returns:
            Timestamp with the format: `%m/%d/%Y, %H:%M:%S`.
        """
        if self.timestamp:
            return self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        return ""
