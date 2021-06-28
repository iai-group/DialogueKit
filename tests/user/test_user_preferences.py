"""Tests for the UserPreferences class."""

import pytest

from dialoguekit.user.user_preferences import UserPreferences
from dialoguekit.core.ontology import Ontology


# User preferences instance to be shared across multiple test cases.
@pytest.fixture
def user_preferences():
    ontology = Ontology("tests/data/ontology.yaml")
    return UserPreferences(ontology)


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
