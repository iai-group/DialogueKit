"""Interface representing user's feedback.

Currently only binary feedback is supported on the utterance level.
Later, it might be extended to graded feedback as well as with
conversation-level feedback.
"""
from dataclasses import dataclass, field
from enum import Enum


class BinaryFeedback(Enum):
    """Represents binary feedback provided by a user."""

    NEGATIVE = 0
    POSITIVE = 1


@dataclass(eq=True, unsafe_hash=True)
class UtteranceFeedback:
    """Represents feedback provided for the utterance."""

    utterance_id: str = field(hash=True)
    feedback: BinaryFeedback = field(hash=True)
