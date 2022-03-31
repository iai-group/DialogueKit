"""General representation of user preferences.

Preferences are given to key-value pairs in terms of real values in [-1,1].
"""

from collections import defaultdict
from typing import Dict, Optional


class UserPreferences:
    def __init__(self, user_id: str) -> None:
        """Initializes the user's preference model.

        Args:
            user_id: User ID.
        """
        self._preferences = defaultdict(dict)

    def set_preference(self, key: str, value: str, preference: float) -> None:
        """Sets (or updates) preference for a given key-value pair.

        Args:
            key: Key.
            value: Value.
            preference: Preference, represented as a float in [-1,1].

        Raises:
            ValueError: Preference is outside the allowed range.
        """
        if preference < -1 or preference > 1:
            raise ValueError("Preference is outside the allowed [-1,1] range")
        self._preferences[key][value] = preference

    def get_preferences(self, key: str) -> Optional[Dict[str, float]]:
        """Returns the preferences on all keys.

        Args:
            key: Key.

        Returns:
            Preferences as key-preference pairs in a dictionary (or None).
        """
        if key in self._preferences:
            return self._preferences[key]
        return None

    def get_preference(self, key: str, value: str) -> Optional[float]:
        """Returns the preference on a key-value pair (or None).

        Args:
            key: Key.
            value: Value.

        Returns:
            Preference, as a float in [-1,1] or None.
        """
        if key in self._preferences:
            if value in self._preferences[key]:
                return self._preferences[key][value]
        return None
