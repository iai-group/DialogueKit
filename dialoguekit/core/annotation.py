"""Interface representing an annotation."""


class Annotation:
    def __init__(self, slot: str = None, value: str = None) -> None:
        """Represents an annotation."""
        self._slot = slot
        self._value = value

    def __str__(self) -> str:
        return f"Annotation({self._slot}, {self._value})"

    def __repr__(self) -> str:
        return f"Annotation({self._slot}, {self._value})"

    def __hash__(self) -> int:
        return hash((self._slot, self._value))

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
        if not isinstance(__o, Annotation):
            return False
        if self._slot != __o._slot:
            return False
        elif self._value != __o._value:
            return False
        return True

    @property
    def slot(self) -> str:
        """Returns the annotation slot."""
        return self._slot

    @property
    def value(self) -> str:
        """Returns the annotation value."""
        return self._value
