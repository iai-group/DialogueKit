"""Interface representing slot-value annotations."""


from dataclasses import dataclass, field

from dialoguekit.core.annotation import Annotation


@dataclass(eq=True, unsafe_hash=True)
class SlotValueAnnotation(Annotation):
    """Represents slot-value annotation."""

    slot: str = field(default=None, hash=True)
    value: str = field(default=None, hash=True)
    start: int = field(default=None, hash=True)
    end: int = field(default=None, hash=True)
