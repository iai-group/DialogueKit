"""Test Intent class"""
import pytest
from dialoguekit.core.intent import Intent


def test_initialization():
    i1 = Intent("test1")
    assert isinstance(i1, Intent)
    assert i1._label == "test1"


def test_label_property():
    i1 = Intent("test1")
    assert i1.label == "test1"


def test_hash():
    i1 = Intent("Test1")
    try:
        hash(i1)
    except TypeError:
        pytest.fail("Intent hashing failed")


def test_comparison():
    i1 = Intent("test1")
    i2 = i1
    assert i1 == i2

    i3 = Intent("test1")
    assert i1 == i3

    i4 = Intent("test2")
    assert i1 != i4
