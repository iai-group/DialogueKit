"""Test Intent class."""
import pytest
from dialoguekit.core import Intent


def test_initialization():
    """Tests intent initialization."""
    i1 = Intent("test1")
    assert isinstance(i1, Intent)
    assert i1._label == "test1"


def test_label_property():
    """Tests intent label."""
    i1 = Intent("test1")
    assert i1.label == "test1"


def test_hash():
    """Tests intent hashing method."""
    i1 = Intent("Test1")
    try:
        hash(i1)
    except TypeError:
        pytest.fail("Intent hashing failed")


def test_comparison():
    """Tests intent comparison."""
    i1 = Intent("test1")
    i2 = i1
    assert i1 == i2

    i3 = Intent("test1")
    assert i1 == i3

    i4 = Intent("test2")
    assert i1 != i4


def test_subintent():
    """Tests intent subintents."""
    i1 = Intent("test1")
    i2 = Intent("test2", main_intent=i1)

    assert i2.main_intent == i1
    assert i1.sub_intents[0] == i2
    assert len(i1.sub_intents) == 1
    assert len(i2.sub_intents) == 0
    assert i1.main_intent is None


def test_subintent_properties():
    """Tests subintent properties."""
    i1 = Intent("test1")
    i2 = Intent("test2", main_intent=i1)

    assert i1.is_main_intent
    assert not i2.is_main_intent

    assert i1.has_sub_intents
    assert not i2.has_sub_intents
