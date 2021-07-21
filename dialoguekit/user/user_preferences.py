"""Representation of user preferences.
Preferences are stored for possible values of slots, as defined by an ontology.
For each slot value, preference is represented as an integer, with negative and
positive numbers corresponding to different degrees of likes and dislikes
(zero means neutral).
"""

import os
import json
import random
from typing import Optional, Dict, Tuple, Any

from dialoguekit.core.ontology import Ontology


def load_db(
    ontology: Ontology, item_file: str, rating_file: str
) -> Tuple[Dict, Dict]:
    """Loads db/json file as backend knowledge.

    Arg:
        item_file: JSON file containing list of items with ratings.

    Return:
        List of items with ratings and list of user preferences.
    """
    if not os.path.isfile(item_file):
        raise FileNotFoundError(f"Item file not found: {item_file}")

    if not os.path.isfile(rating_file):
        raise FileNotFoundError(f"Rating file not found: {rating_file}")

    # TODO: Use ItemCollection instead
    # See https://github.com/iai-group/dialoguekit/issues/37
    # Loads items, a running example:
    # item_id: {"TITLE": title; "GENRE": ["GENRE 1"]; "ACTOR": ["ACTOR 1"]}.
    items = json.load(open(item_file))

    # Loads ratings from the crowd, a running example:
    # item_id: {"USER 1": 5}
    ratings = json.load(open(rating_file))

    # Loads slot names from ontology, i.e, ["TITLE", "GENRE", "ACTOR"].
    slot_names = ontology.get_slot_names()

    # Makes sure the slot names are consistent with the keys in items.
    assert len(items.keys()) > 0
    assert len(ratings.keys()) > 0
    # At least one item have ratings.
    assert len(set(items.keys()).intersection(set(ratings.keys()))) > 0

    crowd_user_preferences = dict()

    # Loads ratings from the crowd, i.e., user id and its rating for this item.
    for item_id, item in items.items():
        item_ratings = ratings.get(item_id, {})
        for user_id, rating in item_ratings.items():
            if user_id not in crowd_user_preferences:
                # Initializes user preferences,
                # i.e. {"TITLE": {}, "GENRE": {}, "ACTOR": {}}.
                crowd_user_preferences[user_id] = {
                    slot_name: dict() for slot_name in slot_names
                }

            # Loads ratings towards each slot name from the rated items.
            for slot_name in slot_names:
                # Slot name's values is a string, e.g., TITLE is a string.
                if isinstance(item.get(slot_name), str):
                    crowd_user_preferences[user_id][slot_name][
                        item.get(slot_name)
                    ] = rating
                # Slot name's values is a list, e.g.
                # A TITLE has multiple GENRE and ACTOR.
                elif isinstance(item.get(slot_name), list):
                    for value in item.get(slot_name):
                        if (
                            value
                            not in crowd_user_preferences[user_id][slot_name]
                        ):
                            crowd_user_preferences[user_id][slot_name][
                                value
                            ] = list()
                        crowd_user_preferences[user_id][slot_name][
                            value
                        ].append(rating)

    return items, crowd_user_preferences


class UserPreferences:
    """Representation of the user's preferences."""

    def __init__(
        self, ontology: Ontology, item_file: str, rating_file: str
    ) -> None:
        """Initializes the user's preference model.
        Args:
            ontology: An ontology.
            item_file: Items records.
            rating_file: Ratings for items in item file.
        """
        # The user can have preferences for specific values for each slot.
        self.__preferences = {
            slot_name: {} for slot_name in ontology.get_slot_names()
        }
        self.items, self.crowd_user_preferences = load_db(
            ontology, item_file, rating_file
        )
        self.user_preferences = self.initialize_preferences()

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

    def initialize_preferences(self, **kwargs) -> None:
        """Initializes the user's preferences via sampling items.

        Arg:
            kwargs: This is intended for debug via assigning preferences
            as this function will randomly sample preferences.
            Todo: to be removed by SZ after integration.
        """

        crowd_user_preferences = (
            kwargs.get("kwargs") if kwargs else self.crowd_user_preferences
        )

        entry_list = list(crowd_user_preferences.items())
        # Randomly samples one user as our initial preferences.
        random_user_id, random_user_preference = random.choice(entry_list)
        self.user_preferences = random_user_preference
        return random_user_preference

    def next_user_slots(
        self, agent_intent: str, agent_slot_values: Dict
    ) -> Dict:
        """Determines the next user slots via loading from the initialized
        preferences or sampling."""
        pass

    def update_preferences(
        self, agent_slot_values: Dict[str, Any], rating: int
    ) -> None:
        """Updates user preferences via adding like/disliked items.

        Args:
            agent_slot_values: Agent slot values,
            e.g. {"TITLE": "name", "GENRE": ["3", "4"]}.
        """
        for slot_name, values in agent_slot_values.items():
            if isinstance(values, str):
                self.user_preferences[slot_name][values] = rating
            elif isinstance(values, list):
                for value in values:
                    if value not in self.user_preferences[slot_name]:
                        self.user_preferences[slot_name][value] = list()
                    self.user_preferences[slot_name][value].append(rating)
