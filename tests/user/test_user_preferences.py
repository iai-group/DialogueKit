"""Tests for the UserPreferences class."""

import pytest

from dialoguekit.user.user_preferences import UserPreferences, load_db
from dialoguekit.core.ontology import Ontology


# User preferences instance to be shared across multiple test cases.
@pytest.fixture
def user_preferences():
    ontology = Ontology("tests/data/ontology.yaml")
    return UserPreferences(ontology, "tests/data/example_movies.json")


def test_unknown_slot(user_preferences):
    with pytest.raises(ValueError):
        user_preferences.set_preference("UNKNOWN", "value", 1)


def test_single_preference(user_preferences):
    user_preferences.set_preference("GENRE", "action", 1)
    assert user_preferences.get_preference("GENRE", "action") == 1


def test_update_preference(user_preferences):
    user_preferences.set_preference("GENRE", "action", 1)
    user_preferences.set_preference("GENRE", "action", 2)
    assert user_preferences.get_preference("GENRE", "action") == 2


def test_load_db(user_preferences):
    # Given
    ontology = Ontology("tests/data/ontology.yaml")
    item_file = "tests/data/example_movies.json"
    user_id = "USER 7"
    expected_user_preferences = {
        "ACTOR": {"Actor 5": [3], "Actor 6": [3], "Actor 7": [3]},
        "GENRE": {"Genre 2": [3], "Genre 4": [3], "Genre 5": [3]},
        "TITLE": {"Movie 3": 3},
    }

    # When
    user_items, crowd_user_preferences = load_db(
        ontology, item_file
    )

    # Then
    assert user_preferences.items
    assert user_preferences.crowd_user_preferences
    assert user_items
    assert crowd_user_preferences
    assert (
        user_preferences.crowd_user_preferences.get(user_id)
        == expected_user_preferences
    )


def test_initialize_preferences(user_preferences):
    assert user_preferences.initialize_preferences()
    assert list(user_preferences.initialize_preferences().keys()) == [
        "TITLE",
        "GENRE",
        "ACTOR",
    ]


def test_update_preferences(user_preferences):
    # Given
    test_user_id = "User test"
    assigned_user_preferences = {
        test_user_id: {
            "ACTOR": {"Actor 5": [3], "Actor 6": [3], "Actor 7": [3]},
            "GENRE": {"Genre 2": [3], "Genre 4": [3], "Genre 5": [3]},
            "TITLE": {"Movie 3": 3},
        }
    }
    new_agent_slot_values = {
        "TITLE": "Movie 4",
        "GENRE": ["Genre 2", "Genre 6"],
    }
    rating = 5

    expected_updated_user_preferences = {
        "ACTOR": {"Actor 5": [3], "Actor 6": [3], "Actor 7": [3]},
        "GENRE": {
            "Genre 2": [3, 5],
            "Genre 4": [3],
            "Genre 5": [3],
            "Genre 6": [5],
        },
        "TITLE": {"Movie 3": 3, "Movie 4": 5},
    }

    # When
    user_preferences_dict = user_preferences.initialize_preferences(
        kwargs=assigned_user_preferences
    )
    user_preferences.update_preferences(new_agent_slot_values, rating)

    # Then
    assert user_preferences_dict == assigned_user_preferences.get(test_user_id)
    assert (
        user_preferences.user_preferences
        == expected_updated_user_preferences
    )
