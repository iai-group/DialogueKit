"""Methods for reading dialogue exports"""

import json
from typing import Any, Dict, List

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue import Dialogue, DialogueParticipant
from dialoguekit.core.intent import Intent

_FIELD_UTTERANCE = "utterance"
_FIELD_INTENT = "intent"
_FIELD_SLOT_VALUES = "slot_values"
_FIELD_CONVERSATION = "conversation"
_FIELD_PARTICIPANT = "participant"


def json_to_annotated_utterance(
    json_utterance: Dict[Any, Any]
) -> AnnotatedUtterance:
    utterance_text = json_utterance.get(_FIELD_UTTERANCE)

    intent = json_utterance.get(_FIELD_INTENT)
    if intent:
        intent = Intent(intent)

    annotations = json_utterance.get(_FIELD_SLOT_VALUES)
    if annotations:
        annotations = [
            Annotation(slot=slot, value=value) for slot, value in annotations
        ]

    satisfaction = json_utterance.get("satisfaction")

    return AnnotatedUtterance(
        text=utterance_text,
        annotations=annotations,
        intent=intent,
        metadata={"satisfaction": satisfaction}
    )


def json_to_dialogues(
    filepath: str, agent_id: str, user_id: str
) -> List[Dialogue]:
    f = open(filepath)
    data = json.load(f)

    dialogues = []
    for dialogue_data in data:
        dialogue_history = Dialogue(agent_id, user_id)
        for utterance_data in dialogue_data.get(_FIELD_CONVERSATION):
            participant = utterance_data.get(_FIELD_PARTICIPANT)
            annotated_utterance = json_to_annotated_utterance(utterance_data)
            if participant == DialogueParticipant.AGENT.name:
                dialogue_history.add_agent_utterance(annotated_utterance)
            elif participant == DialogueParticipant.USER.name:
                dialogue_history.add_user_utterance(annotated_utterance)
        dialogues.append(dialogue_history)

    return dialogues
