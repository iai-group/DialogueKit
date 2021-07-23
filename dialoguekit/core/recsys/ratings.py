"""Represents item ratings and provides access either based on items or on
users."""

import csv
from collections import defaultdict
from typing import Dict, Optional

from dialoguekit.core.recsys.item_collection import ItemCollection


class Ratings:
    def __init__(self, item_collection: ItemCollection = None) -> None:
        self._item_collection = item_collection
        self._item_ratings = defaultdict(dict)
        self._user_ratings = defaultdict(dict)

    def load_ratings_csv(self, file_path: str, delimiter: str = ",") -> None:
        """Loads ratings from a csv file.

        The file is assumed to have userID, itemID, and rating columns
        (following the MovieLens format). Additional columns that may be present
        are ignored. UserID and itemID are strings, rating is a float.

        If an ItemCollection is provided in the constructor, then ratings are
        filtered to items that are present in the collection.

        Args:
            file_path: Path to CSV file.
            delimiter: Field separator (default: comma).
        """
        with open(file_path, "r") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter)
            heading = next(csvreader)
            if len(heading) < 3:
                raise ValueError("Invalid CSV format (too few columns).")
            for values in csvreader:
                user_id, item_id = values[:2]
                rating = float(values[2])
                # Filters items based on their existence in ItemCollection.
                if self._item_collection:
                    if not self._item_collection.exists(item_id):
                        continue
                self._item_ratings[item_id][user_id] = rating
                self._user_ratings[user_id][item_id] = rating

    def get_user_ratings(self, user_id: str) -> Dict[str, float]:
        """Returns all ratings of a given user.

        Args:
            user_id: User ID.

        Returns:
            Dictionary with item IDs as keys and ratings as values.
        """
        return self._user_ratings[user_id]

    def get_item_ratings(self, item_id: str) -> Dict[str, float]:
        """Returns all ratings given to a specific item.

        Args:
            item_id: Item ID.

        Returns:
            Dictionary with user IDs as keys and ratings as values.
        """
        return self._item_ratings[item_id]

    def get_user_item_rating(
        self, user_id: str, item_id: str
    ) -> Optional[float]:
        """Returns the rating by a given user on a specific item.

        Args:
            user_id: User ID.
            item_id: Item ID.

        Returns:
            Rating as float or None.
        """
        return self._user_ratings[user_id].get(item_id, None)
