"""Interface representing an annotation."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(eq=True, unsafe_hash=True)
class Annotation:
    """Represents an annotation."""

    key: str = field(default=None, hash=True)
    value: Any = field(default=None, hash=True)
