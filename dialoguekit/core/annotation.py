"""Interface representing an annotation."""


from dataclasses import dataclass, field


@dataclass(eq=True, unsafe_hash=True)
class Annotation:
    """Represents an annotation."""

    slot: str = field(default=None, hash=True)
    value: str = field(default=None, hash=True)
