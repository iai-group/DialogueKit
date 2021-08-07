"""Tests for the UserPreferences class."""

import pytest

from dialoguekit.user.user_preferences import UserPreferences


def test_set_preference():
    user_preferences = UserPreferences("user0")
    assert not user_preferences.get_preference("key1", "value1")
    user_preferences.set_preference("key1", "value1", 1)
    assert user_preferences.get_preference("key1", "value1") == 1
    user_preferences.set_preference("key1", "value1", 0.5)
    assert user_preferences.get_preference("key1", "value1") == 0.5


def test_get_preferences():
    user_preferences = UserPreferences("user1")
    user_preferences.set_preference("key1", "value1", 1)
    user_preferences.set_preference("key1", "value2", 0.5)
    assert user_preferences.get_preferences("key1") == {
        "value1": 1,
        "value2": 0.5,
    }
    assert not user_preferences.get_preferences("key2")


def test_preference_range():
    user_preferences = UserPreferences("user2")
    with pytest.raises(ValueError):
        user_preferences.set_preference("k", "v", -2)
    with pytest.raises(ValueError):
        user_preferences.set_preference("k", "v", 1.05)
