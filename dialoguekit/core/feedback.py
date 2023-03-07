"""Interface representing user's feedback."""
from dataclasses import dataclass, field
from enum import Enum


class BinaryFeedback(Enum):
    """Represents user's feedback."""

    NEGATIVE = 0
    POSITIVE = 1

@dataclass(eq=True, unsafe_hash=True)
class UtteranceFeedback:
    """Represents a feedback provided for an utterance."""

    utterance_id: str = field(hash=True)
    feedback: BinaryFeedback = field(hash=True)