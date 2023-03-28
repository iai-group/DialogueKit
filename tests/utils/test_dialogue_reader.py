"""Tests for the dialogue reader."""

from dialoguekit.core.intent import Intent
from dialoguekit.utils.dialogue_reader import json_to_dialogues


def test_json_to_dialogues():
    """Tests reading of json dialogues."""
    dialogues = json_to_dialogues(
        filepath="tests/data/annotated_dialogues.json",
        agent_id="TestAGENT",
        user_id="TestUSER",
    )
    assert len(dialogues) == 3
    assert len(dialogues[0].utterances) > 0
    assert dialogues[0].utterances[0].participant == "USER"
    assert dialogues[0].utterances[1].participant == "AGENT"
    assert dialogues[0].utterances[0].get_intents() == [
        Intent("DISCLOSE.NON-DISCLOSE")
    ]
    assert dialogues[0].utterances[1].get_intents() == [
        Intent("INQUIRE.ELICIT")
    ]
