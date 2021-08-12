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
