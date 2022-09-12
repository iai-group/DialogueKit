"""Interface representing an intent."""


from typing import Any, List, Optional, Text, Union


class Intent:
    def __init__(
        self, label: str, main_intent: Optional[Union[None, Any]] = None
    ) -> None:
        """Initializes the intent.

        Args:
            label: Intent label.
            main_intent: The main_intent intent.
        """
        self._label = label
        self._main_intent = main_intent
        if self._main_intent:
            self._main_intent._add_sub_intent(sub_intent=self)

        self._sub_intents: List[Any] = []

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
        if self._main_intent != __o._main_intent:
            return False
        if len(self._sub_intents) != len(__o.sub_intents):
            return False
        if len(set(self._sub_intents) - set(__o.sub_intents)) != 0:
            return False
        return True

    @property
    def label(self) -> str:
        """Returns the Intent label."""
        return self._label

    @property
    def main_intent(self) -> Union[Any, None]:
        """Returns the main intent."""
        return self._main_intent

    @property
    def sub_intents(self) -> List[Any]:
        """Returns a list of sub-intents."""
        return self._sub_intents

    @property
    def is_main_intent(self) -> bool:
        """Returns bool if it is the main intent."""
        return self.main_intent is None

    @property
    def has_sub_intents(self) -> bool:
        """Returns bool if intent has sub intents."""
        return True if self.sub_intents else False

    def _add_sub_intent(self, sub_intent: Any) -> None:
        """Adds a sub-intent."""
        self._sub_intents.append(sub_intent)
