"""Tests slot_value_annotation class"""
import pytest
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation


def test_initialization():
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    assert isinstance(a1, SlotValueAnnotation)
    assert a1._value == "test1"
    assert a1._slot == "slot1"
    assert a1._start == 0
    assert a1._end == 1


def test_properties():
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    assert a1.slot == "slot1"
    assert a1.value == "test1"


def test_comparison():
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    a2 = a1
    assert a1 == a2

    a3 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    assert a1 == a3

    # Test value difference
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    a2 = SlotValueAnnotation(value="test2", slot="slot1", start=0, end=1)
    assert a1 != a2

    # Test slot difference
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    a2 = SlotValueAnnotation(value="test1", slot="slot2", start=0, end=1)
    assert a1 != a2

    # Test start difference
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    a2 = SlotValueAnnotation(value="test1", slot="slot1", start=1, end=1)
    assert a1 != a2

    # Test end difference
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    a2 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=2)
    assert a1 != a2


def test_hash():
    a1 = SlotValueAnnotation(value="test1", slot="slot1", start=0, end=1)
    try:
        hash(a1)
    except TypeError:
        pytest.fail("SlotValueAnnotation hashing failed")
