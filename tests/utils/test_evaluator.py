"""Tests the dialogue evaluation."""

from typing import Any, Dict, List

import pytest

from dialoguekit.core.dialogue import Dialogue
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlu import SatisfactionClassifierSVM
from dialoguekit.participant import DialogueParticipant
from dialoguekit.utils import Evaluator
from dialoguekit.utils.dialogue_reader import json_to_dialogues


@pytest.fixture
def annotated_dialogues() -> List[Dialogue]:
    """Test dialogue fixture."""
    export_dialogues = json_to_dialogues(
        filepath="tests/data/annotated_dialogues.json",
    )
    return export_dialogues


@pytest.fixture
def reward_config() -> Dict[str, Any]:
    """Test reward config."""
    _REWARD_CONFIG = {
        "full_set_points": 20,
        "intents": {
            "DISCLOSE": 4,
            "REVEAL.REFINE": 4,
            "INQUIRE": 4,
            "NAVIGATE": 4,
        },
        "repeat_penalty": 1,
        "cost": 1,
    }
    return _REWARD_CONFIG


@pytest.fixture
def satisfaction_classifier() -> SatisfactionClassifierSVM:
    """Tests satisfaction classifier init.

    Also used as a fixture for the tests.
    """
    return SatisfactionClassifierSVM()


def test_init(
    annotated_dialogues: List[Dialogue], reward_config: Dict[str, Any]
) -> None:
    """Tests evaluator initialization.

    Args:
        annotated_dialogues: Test dialogue object.
        reward_config: Test reward config.
    """
    Evaluator(dialogues=annotated_dialogues, reward_config=reward_config)


def test_avg_turns(
    annotated_dialogues: List[Dialogue], reward_config: Dict[str, Any]
) -> None:
    """Tests avg_turns method.

    Args:
        annotated_dialogues: Test dialogue object.
        reward_config: Test reward config.
    """
    ev = Evaluator(dialogues=annotated_dialogues, reward_config=reward_config)
    avg_turns = ev.avg_turns()
    assert avg_turns == pytest.approx(16.33, 0.1)
    avg_turns2 = ev.avg_turns()
    assert avg_turns2 == pytest.approx(16.33, 0.1)


def test_user_act_ratio(
    annotated_dialogues: List[Dialogue], reward_config: Dict[str, Any]
) -> None:
    """Tests user action ratio method.

    Args:
        annotated_dialogues: Test dialogue object.
        reward_config: Test reward config.
    """
    ev = Evaluator(dialogues=annotated_dialogues, reward_config=reward_config)
    stats = ev.user_act_ratio()

    assert stats
    assert "AGENT/USER" in list(stats.keys())
    assert stats.get("USER") == 50
    assert stats.get("USER/AGENT") == pytest.approx(0.84, 0.1)


def test_reward(
    annotated_dialogues: List[Dialogue], reward_config: Dict[str, Any]
) -> None:
    """Tests reward calculation.

    Args:
        annotated_dialogues: Test dialogue object.
        reward_config: Test reward config.
    """
    ev = Evaluator(dialogues=annotated_dialogues, reward_config=reward_config)
    rewards = ev.reward()
    assert len(rewards["dialogues"]) == len(annotated_dialogues)
    for reward in rewards["dialogues"]:
        assert reward["reward"] >= 0


def test_reward_type_error(reward_config: Dict[str, Any]) -> None:
    """Tests reward calculation.

    Args:
        reward_config: Test reward config.
    """
    dialogue = Dialogue("AGENT01", "USER01", "CNV1")
    dialogue.add_utterance(
        Utterance(
            "Hello, which genres do you prefer?", DialogueParticipant.AGENT
        )
    )
    dialogue.add_utterance(Utterance("Hello", DialogueParticipant.USER))
    ev = Evaluator(dialogues=[dialogue], reward_config=reward_config)

    with pytest.raises(TypeError):
        ev.reward()


def test_satisfaction_classification(
    annotated_dialogues: List[Dialogue],
    reward_config: Dict[str, Any],
    satisfaction_classifier: SatisfactionClassifierSVM,
) -> None:
    """Tests satisfaction classification.

    Args:
        annotated_dialogues: Test dialogue object.
        reward_config: Test reward config.
        satisfaction_classifier: Satisfaction classifier.
    """
    ev = Evaluator(dialogues=annotated_dialogues, reward_config=reward_config)
    satisfactions = ev.satisfaction(satisfaction_classifier)
    print(satisfactions)
    assert satisfactions
    for sc in satisfactions:
        assert 1 <= sc <= 5
