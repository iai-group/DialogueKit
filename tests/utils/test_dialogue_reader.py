"""Tests for the dialogue reader."""

from dialoguekit.core.intent import Intent
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
    assert dialogues[0].utterances[0].get_intents() == [
        Intent("DISCLOSE.NON-DISCLOSE")
    ]
    assert dialogues[0].utterances[1].get_intents() == [
        Intent("INQUIRE.ELICIT")
    ]
