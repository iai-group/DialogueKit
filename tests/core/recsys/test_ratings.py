"""Tests for Ratings."""

import pytest

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
        "5": pytest.approx(-0.333, rel=1e-2),  # 2
        "12": pytest.approx(0.555, rel=1e-2),  # 4
        "24": 1.0,  # 5
        "25": pytest.approx(-0.111, rel=1e-2),  # 2.5,
        "27": pytest.approx(0.555, rel=1e-2),  # 4
    }

    # Checks ratings by a given user.
    assert ratings.get_user_ratings("28") == {
        "150": pytest.approx(-0.777, rel=1e-2),  # 1
        "161": pytest.approx(0.111, rel=1e-2),  # 3
        "165": pytest.approx(0.111, rel=1e-2),  # 3
        "185": pytest.approx(-0.777, rel=1e-2),  # 1
        "196": pytest.approx(-0.777, rel=1e-2),  # 1
        "213": 1.0,  # 5
        "231": pytest.approx(0.111, rel=1e-2),  # 3
    }

    # Checks ratings on specific user-item pairs.
    assert ratings.get_user_item_rating("1", "2") == pytest.approx(
        0.333, rel=1e-2
    )  # 3.5
    assert ratings.get_user_item_rating("14", "911") == pytest.approx(
        0.555, rel=1e-2
    )  # 4
