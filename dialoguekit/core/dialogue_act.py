"""Interface representing a dialogue act."""

from ast import List
from dataclasses import dataclass, field

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent


@dataclass(eq=True, unsafe_hash=True)
class DialogueAct:
    """Represents a dialogue act that is an intent and its annotations."""

    intent: Intent = field(default=None, hash=True)
    annotations: List[Annotation] = field(
        default_factory=list, compare=True, hash=False
    )
