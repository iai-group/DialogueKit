"""Tests for preference model."""

import pytest

from dialoguekit.user.preference_model import PreferenceModel, load_db


# preference model class shared across tests.
@pytest.fixture
def preference_model_class():
    return PreferenceModel(
        "tests/data/ontology.yaml", "tests/data/example_movies.json"
    )


def test_load_db(preference_model_class):
    # Given
    ontology_config_file = "tests/data/ontology.yaml"
    item_file = "tests/data/example_movies.json"
    user_id = "USER 7"
    expected_user_preferences = {
        "ACTOR": {"Actor 5": [3], "Actor 6": [3], "Actor 7": [3]},
        "GENRE": {"Genre 2": [3], "Genre 4": [3], "Genre 5": [3]},
        "TITLE": {"Movie 3": 3},
    }

    # When
    user_items, crowd_user_preferences = load_db(
        ontology_config_file, item_file
    )

    # Then
    assert preference_model_class.items
    assert preference_model_class.crowd_user_preferences
    assert user_items
    assert crowd_user_preferences
    assert (
        preference_model_class.crowd_user_preferences.get(user_id)
        == expected_user_preferences
    )


def test_initialize_preferences(preference_model_class):
    assert preference_model_class.initialize_preferences()
    assert list(preference_model_class.initialize_preferences().keys()) == [
        "TITLE",
        "GENRE",
        "ACTOR",
    ]


def test_update_preferences(preference_model_class):
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
    user_preferences = preference_model_class.initialize_preferences(
        kwargs=assigned_user_preferences
    )
    preference_model_class.update_preferences(new_agent_slot_values, rating)

    # Then
    assert user_preferences == assigned_user_preferences.get(test_user_id)
    assert (
        preference_model_class.user_preferences
        == expected_updated_user_preferences
    )
