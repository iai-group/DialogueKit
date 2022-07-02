"""Interface representing an intent."""


from typing import Text, Optional, Any, Union, List


class Intent:
    def __init__(
        self, label: str, parent: Optional[Union[None, Any]] = None
    ) -> None:
        """Initializes the intent.

        Args:
            label: Intent label.
            parent
        """
        self._label = label
        self._parent = parent
        if self._parent:
            self._parent._add_child_intent(self)

        self._children = []

    def __str__(self) -> Text:
        return self._label

    def __repr__(self) -> Text:
        return f"Intent({self._label})"

    def __hash__(self) -> int:
        return hash(self._label)

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
        if not isinstance(__o, Intent):
            return False
        if self._label != __o._label:
            return False
        if self._parent != __o._parent:
            return False
        if len(self._children) != len(__o.children):
            return False
        if len(set(self._children) - set(__o.children)) != 0:
            return False
        return True

    @property
    def label(self) -> str:
        return self._label

    @property
    def parent(self) -> Any:
        return self._parent

    @property
    def children(self) -> List[Any]:
        return self._children

    def _add_child_intent(self, child: Any) -> None:
        self._children.append(child)
