"""Interface representing slot-value annotations."""


from typing import Text
from dialoguekit.core.annotation import Annotation


class SlotValueAnnotation(Annotation):
    """Represents slot-value annotation."""

    def __init__(
        self,
        slot: str = None,
        value: str = None,
        start: int = None,
        end: int = None,
    ) -> None:
        # TODO Connect to Ontology (and restrict to slots in there)?
        super().__init__(slot=slot, value=value)
        self._start = start
        self._end = end

    def __str__(self) -> Text:
        return f"SlotValueAnnotation({self._slot}, {self._value}, \
            {self._start}, {self._end})"

    def __repr__(self) -> Text:
        return f"SlotValueAnnotation({self._slot}, {self._value}, \
            {self._start}, {self._end})"

    def __hash__(self) -> int:
        return hash((super().__hash__(), self._start, self._end))

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
        if not isinstance(__o, SlotValueAnnotation):
            return False
        if self._slot != __o._slot:
            return False
        elif self._value != __o._value:
            return False
        elif self._start != __o._start:
            return False
        elif self._end != __o._end:
            return False

        return True
