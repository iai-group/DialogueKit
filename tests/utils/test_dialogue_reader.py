"Tests for the dialogue reader"

from dialoguekit.utils.dialogue_reader import json_to_dialogues


def test_json_to_dialogues():
    dialogues = json_to_dialogues(
        filepath="tests/data/annotated_dialogues.json",
        agent_id="TestAGENT",
        user_id="TestUSER",
    )
    assert len(dialogues) == 3
    assert len(dialogues[0].utterances) > 0
