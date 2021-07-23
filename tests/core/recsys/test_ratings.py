"""Tests for Ratings."""

from dialoguekit.core.recsys.ratings import Ratings

RATINGS_CSV_FILE = "tests/data/movielens-20m-sample/ratings.csv"


def test_empty_ratings():
    ratings = Ratings()
    assert not ratings.get_user_ratings("1")
    assert not ratings.get_item_ratings("2")


def test_load_ratings_csv():
    ratings = Ratings()
    ratings.load_ratings_csv(RATINGS_CSV_FILE)

    # Checks ratings on a given item.
    assert ratings.get_item_ratings("104") == {
        "5": 2,
        "12": 4,
        "24": 5,
        "25": 2.5,
        "27": 4,
    }

    # Checks ratings by a given user.
    assert ratings.get_user_ratings("28") == {
        "150": 1,
        "161": 3,
        "165": 3,
        "185": 1,
        "196": 1,
        "213": 5,
        "231": 3,
    }

    # Checks ratings on specific user-item pairs.
    assert ratings.get_user_item_rating("1", "2") == 3.5
    assert ratings.get_user_item_rating("14", "911") == 4
