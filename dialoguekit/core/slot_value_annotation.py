"""Interface representing slot-value annotations."""

from dataclasses import dataclass, field
from typing import Optional

from dialoguekit.core.annotation import Annotation


@dataclass(eq=True, unsafe_hash=True)
class SlotValueAnnotation(Annotation):
    """Represents slot-value annotation."""

    slot: str = field(default=None, hash=True)
    start: int = field(default=None, hash=True)
    end: int = field(default=None, hash=True)

    def __init__(
        self,
        slot: str,
        value: Optional[str] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> None:
        """Instantiates a slot-value annotation.

        Args:
            slot: Slot name.
            value: Slot value. Defaults to None.
            start: Start index of the slot value in the utterance. Defaults to
              None.
            end: End index of the slot value in the utterance. Defaults to None.
        """
        super().__init__(key=slot, value=value)
        self.slot = slot
        self.start = start
        self.end = end
