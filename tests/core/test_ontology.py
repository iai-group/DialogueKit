"""Tests for the DialogueHistory class."""

import pytest
from dialoguekit.core.domain import Domain


# Sample domain to be shared across multiple test cases.
@pytest.fixture
def sample_domain():
    return Domain("tests/data/domains/movie.yaml")


def test_class_names(sample_domain):
    assert sample_domain.get_slot_names() == ["TITLE", "GENRE", "ACTOR"]
