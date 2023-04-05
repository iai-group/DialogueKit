"""Tests for the dialogue reader."""

import pytest

from dialoguekit.utils.dialogue_reader import json_to_dialogues


def test_json_to_dialogues() -> None:
    """Tests reading of json dialogues."""
    dialogues = json_to_dialogues(
        filepath="tests/data/annotated_dialogues.json",
    )
    assert len(dialogues) == 3
    assert len(dialogues[0].utterances) > 0
    assert dialogues[0].agent_id == "MovieBotTester"
    assert dialogues[0].user_id == "TEST03"
    assert dialogues[-1].agent_id == "Agent"
    assert dialogues[-1].user_id == "User"
    assert dialogues[0].utterances[0].participant == "USER"
    assert dialogues[0].utterances[1].participant == "AGENT"
    assert dialogues[0].utterances[0].intent.label == "DISCLOSE.NON-DISCLOSE"
    assert dialogues[0].utterances[1].intent.label == "INQUIRE.ELICIT"


@pytest.mark.parametrize(
    "agent_id, user_id, expected_dialogue_count",
    [
        ("MovieBotTester", None, 1),
        (None, None, 3),
        ("TestAgent", "TestUser", 0),
        (None, "TEST03", 1),
        ("MovieBotTester", "TEST03", 1),
    ],
)
def test_json_to_dialogues_filtered(
    agent_id: str, user_id: str, expected_dialogue_count: int
) -> None:
    """Tests reading of json dialogues with filtering parameters."""
    dialogues = json_to_dialogues(
        filepath="tests/data/annotated_dialogues.json",
        agent_id=agent_id,
        user_id=user_id,
    )
    assert len(dialogues) == expected_dialogue_count
