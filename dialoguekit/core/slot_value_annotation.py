"""Interface representing slot-value annotations."""


class SlotValueAnnotation:
    """Represents slot-value annotation."""

    def __init__(
        self,
        slot: str = None,
        value: str = None,
        start: int = None,
        end: int = None,
    ) -> None:
        # TODO Connect to Ontology (and restrict to slots in there)?
        self._slot = slot
        self._value = value
        self._start = start
        self._end = end

    @property
    def slot(self) -> str:
        return self._slot

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, __o: object) -> bool:
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
