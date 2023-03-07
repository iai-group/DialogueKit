"""Tests for the Domain class."""

import pytest

from dialoguekit.core import Domain


@pytest.fixture
def sample_domain():
    """Domain fixture."""
    return Domain("tests/data/domains/movie.yaml")


def test_get_slot_names(sample_domain: Domain) -> None:
    """Tests get_slot_names method."""
    assert sample_domain.get_slot_names() == ["TITLE", "GENRE", "ACTOR"]


def test_get_name(sample_domain: Domain) -> None:
    """Tests get_name method."""
    assert "Movie" == sample_domain.get_name()
