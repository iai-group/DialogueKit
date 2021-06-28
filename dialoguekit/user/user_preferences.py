"""Representation of user preferences.

Preferences are stored for possible values of slots, as defined by an ontology.
For each slot value, preference is represented as an integer, with negative and
positive numbers corresponding to different degrees of likes and dislikes
(zero means neutral).
"""

from typing import Optional

from dialoguekit.core.ontology import Ontology


class UserPreferences:
    """Representation of a given user's preferences."""

    def __init__(self, ontology: Ontology) -> None:
        """Initializes the user's preference model.

        Args:
            ontology: An ontology.
        """
        # The user can have preferences for specific values for each slot.
        self.__preferences = {
            slot_name: {} for slot_name in ontology.get_slot_names()
        }

    def set_preference(
        self, slot_name: str, slot_value: str, preference: int
    ) -> None:
        """Sets (or updates) preference for a given entity.

        Args:
            slot_name: Slot name.
            slot_value: Slot value (for which preference is set).
            preference: Preference, represented as an int (negative
                value=dislike, 0=neutral, positive value=like).

        Raises:
            ValueError: Unknown slot (not present in the ontology).
        """
        if slot_name not in self.__preferences:
            raise ValueError(f"Unknown slot: {slot_name}")
        self.__preferences[slot_name][slot_value] = preference

    def get_preference(self, slot_name: str, slot_value: str) -> Optional[int]:
        """Determines the preference for a given entity.

        Args:
            slot_name: Slot name.
            slot_value: Slot value.

        Returns:
            Preference, as an int (negative value=dislike, 0=neutral,
                positive value=like) or None .
        """
        return self.__preferences[slot_name][slot_value]
