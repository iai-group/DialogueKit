"""Tests for the DialogueHistory class."""

import pytest

from dialoguekit.core.ontology import Ontology


# Sample ontology to be shared across multiple test cases.
@pytest.fixture
def sample_ontology():
    return Ontology("tests/data/ontology.yaml")


def test_class_names(sample_ontology):
    assert sample_ontology.get_slot_names() == ["TITLE", "GENRE", "ACTOR"]
