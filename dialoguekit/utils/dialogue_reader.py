"""Methods for reading dialogue exports."""

import json
from typing import Any, Dict, List

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue import Dialogue
from dialoguekit.core.intent import Intent

_FIELD_UTTERANCE = "utterance"
_FIELD_UTTERANCE_ID = "utterance_id"
_FIELD_INTENT = "intent"
_FIELD_SLOT_VALUES = "slot_values"
_FIELD_CONVERSATION = "conversation"
_FIELD_CONVERSATION_ID = "conversation_id"
_FIELD_PARTICIPANT = "participant"
_FIELD_AGENT = "agent"
_FIELD_USER = "user"


def json_to_annotated_utterance(
    json_utterance: Dict[Any, Any]
) -> AnnotatedUtterance:
    """Converts an utterance from JSON format to AnnotatedUtterance.

    Args:
        json_utterance: JSON format of an utterance, e.g.,

            .. code:: python

                {
                    "participant": "USER",
                    "utterance": "hello",
                    "intent": "DISCLOSE.NON-DISCLOSE"
                }

    Returns:
        An AnnotatedUtterance object representation of the json utterance.
    """
    participant = json_utterance.get(_FIELD_PARTICIPANT)

    utterance_text = json_utterance.get(_FIELD_UTTERANCE)
    utterance_id = json_utterance.get(_FIELD_UTTERANCE_ID)

    intent = json_utterance.get(_FIELD_INTENT)
    if intent:
        intent = Intent(intent)

    annotations = json_utterance.get(_FIELD_SLOT_VALUES)
    if annotations:
        annotations = [
            Annotation(slot=slot, value=value) for slot, value in annotations
        ]
    metadata = {}
    for k, v in json_utterance.items():
        if k not in (
            [
                _FIELD_UTTERANCE,
                _FIELD_PARTICIPANT,
                _FIELD_SLOT_VALUES,
                _FIELD_INTENT,
            ]
        ):
            metadata[k] = v

    return AnnotatedUtterance(
        text=utterance_text,
        utterance_id=utterance_id,
        participant=participant,
        annotations=annotations,
        intent=intent,
        metadata=metadata,
    )


def json_to_dialogues(
    filepath: str,
    agent_ids: List[str] = None,
    user_ids: List[str] = None,
) -> List[Dialogue]:
    """Parses a JSON file containing dialogues.

    Args:
        filepath: Path to JSON file containing the dialogues.
        agent_ids: List of agents' id to filter loaded dialogues. Defaults to
          None.
        user_ids: List of users' id to filter loaded dialogues. Defaults to
          None.

    Returns:
        A list of Dialogue objects.
    """
    f = open(filepath, encoding="utf-8")
    data = json.load(f)

    dialogues = []
    for dialogue_data in data:
        conversation_id = dialogue_data.get(_FIELD_CONVERSATION_ID, None)
        agent_id = dialogue_data.get(_FIELD_AGENT, {}).get("id", "Agent")
        user_id = dialogue_data.get(_FIELD_USER, {}).get("id", "User")
        if (agent_ids and agent_id not in agent_ids) or (
            user_ids and user_id not in user_ids
        ):
            # Filter loaded dialogues based on agent_ids and/or user_ids if
            # provided
            continue
        dialogue = Dialogue(agent_id, user_id, conversation_id)
        for utterance_data in dialogue_data.get(_FIELD_CONVERSATION):
            annotated_utterance = json_to_annotated_utterance(utterance_data)
            dialogue.add_utterance(annotated_utterance)
        dialogues.append(dialogue)

    return dialogues
