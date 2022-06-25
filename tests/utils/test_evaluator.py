"""Tests the dialogue evaluation"""
import pytest
from dialoguekit.utils.dialogue_evaluation import Evaluator
from dialoguekit.utils.dialogue_reader import json_to_dialogues


@pytest.fixture
def dialogues():
    export_dialogues = json_to_dialogues(
        filepath="tests/data/annotated_dialogues.json",
        agent_id="TestAGENT",
        user_id="TestUSER",
    )
    return export_dialogues


def test_init():
    Evaluator(dialogue_history=dialogues)


def test_avg_turns(dialogues):
    ev = Evaluator(dialogue_history=dialogues)
    avg_turns = ev.avg_turns(dialogue_history=dialogues)
    assert avg_turns == pytest.approx(19.66, 0.1)
    avg_turns2 = ev.avg_turns(dialogue_history=dialogues)
    assert avg_turns2 == pytest.approx(19.66, 0.1)


def test_user_act_ratio(dialogues):
    ev = Evaluator(dialogue_history=dialogues)
    stats = ev.user_act_ratio(dialogue_history=dialogues)

    assert stats
    assert "AGENT/USER" in list(stats.keys())
    assert stats.get("USER") == 50
    assert stats.get("USER/AGENT") == pytest.approx(0.84, 0.1)


def test_reward(dialogues):
    ev = Evaluator(dialogue_history=dialogues)
    rewards = ev.reward(dialogue_history=dialogues)
    assert len(rewards["dialogues"]) == len(dialogues)
    for reward in rewards["dialogues"]:
        assert reward["reward"] >= 0


# def test_satisfaction_classification(dialogues):
#     ev = Evaluator(dialogue_history=dialogues)
#     satisfactions = ev.satisfaction(dialogues)
#     print(satisfactions)
#     assert satisfactions
#     for sc in satisfactions:
#         assert 1 <= sc <= 5
