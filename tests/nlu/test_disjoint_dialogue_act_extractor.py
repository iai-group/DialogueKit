"""Tests for disjoint dialogue act extractor."""

from unittest.mock import Mock

import pytest

from dialoguekit.core.intent import Intent
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlu.disjoint_dialogue_act_extractor import (
    DisjointDialogueActExtractor,
)
from dialoguekit.participant.participant import DialogueParticipant


@pytest.fixture
def intent_classifier() -> Mock:
    """Mock intent classifier."""
    intent_classifier = Mock()
    intent_classifier.classify_intent.return_value = Intent("DISCLOSE")
    return intent_classifier


@pytest.fixture
def slot_value_annotator() -> Mock:
    """Mock slot value annotator."""
    slot_value_annotator = Mock()
    slot_value_annotator.get_annotations.return_value = [
        SlotValueAnnotation("GENRE", "action")
    ]
    return slot_value_annotator


@pytest.fixture
def dialogue_act_extractor(
    intent_classifier: Mock, slot_value_annotator: Mock
) -> DisjointDialogueActExtractor:
    """Dialogue act extractor fixture."""
    return DisjointDialogueActExtractor(
        intent_classifier, [slot_value_annotator]
    )


def test_extract_dialogue_acts(
    dialogue_act_extractor: DisjointDialogueActExtractor,
) -> None:
    """Test dialogue act extraction."""
    utterance = Utterance(
        "I am looking for an action movie", DialogueParticipant.USER
    )
    extracted_dialogue_acts = dialogue_act_extractor.extract_dialogue_acts(
        utterance
    )
    assert len(extracted_dialogue_acts) == 1
    assert extracted_dialogue_acts[0].intent == Intent("DISCLOSE")
    assert extracted_dialogue_acts[0].annotations == [
        SlotValueAnnotation("GENRE", "action")
    ]


def test_extract_dialogue_acts_no_intent(
    dialogue_act_extractor: DisjointDialogueActExtractor,
) -> None:
    """Test dialogue act extraction with no intent."""
    utterance = Utterance(
        "I am looking for an action movie", DialogueParticipant.USER
    )
    dialogue_act_extractor._intent_classifier.classify_intent.return_value = (
        None
    )
    extracted_dialogue_acts = dialogue_act_extractor.extract_dialogue_acts(
        utterance
    )
    assert len(extracted_dialogue_acts) == 0
    assert extracted_dialogue_acts == []
