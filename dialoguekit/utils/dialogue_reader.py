"""Methods for reading dialogue exports."""

import json
from typing import Any, Dict, List

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue import Dialogue
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.feedback import BinaryFeedback, UtteranceFeedback
from dialoguekit.core.intent import Intent
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation
from dialoguekit.participant import DialogueParticipant

_FIELD_UTTERANCE = "utterance"
_FIELD_DIALOGUE_ACTS = "dialogue_acts"
_FIELD_UTTERANCE_ID = "utterance_id"
_FIELD_UTTERANCE_FEEDBACK = "utterance_feedback"
_FIELD_INTENT = "intent"
_FIELD_SLOT_VALUES = "slot_values"
_FIELD_ANNOTATIONS = "annotations"
_FIELD_CONVERSATION = "conversation"
_FIELD_CONVERSATION_ID = "conversation_id"
_FIELD_PARTICIPANT = "participant"
_FIELD_AGENT = "agent"
_FIELD_USER = "user"
_FIELD_METADATA = "metadata"


def json_to_annotated_utterance(
    json_utterance: Dict[Any, Any]
) -> AnnotatedUtterance:
    """Converts an utterance from JSON format to AnnotatedUtterance.

    Args:
        json_utterance: JSON format of an utterance, e.g.,

            .. code:: python

                {
                    "participant": "USER",
                    "utterance": "I like action movies.",
                    "dialogue_acts":
                        [
                            {
                                "intent": "DISCLOSE",
                                "slot_values": [
                                    [
                                        "GENRE",
                                        "action",
                                        7,
                                        13
                                    ]
                                ]
                            }
                        ]
                }

    Returns:
        An AnnotatedUtterance object representation of the json utterance.
    """
    participant = DialogueParticipant[json_utterance.get(_FIELD_PARTICIPANT)]

    utterance_text = json_utterance.get(_FIELD_UTTERANCE)
    utterance_id = json_utterance.get(_FIELD_UTTERANCE_ID)

    dialogue_acts = list()
    for da in json_utterance.get(_FIELD_DIALOGUE_ACTS, []):
        intent = da.get(_FIELD_INTENT)
        if intent:
            intent = Intent(intent)

        annotations = da.get(_FIELD_SLOT_VALUES, [])
        if annotations:
            annotations = [
                SlotValueAnnotation(slot, value, start, end)
                for slot, value, start, end in annotations
            ]

        dialogue_acts.append(DialogueAct(intent, annotations))

    annotations = json_utterance.get(_FIELD_ANNOTATIONS, [])
    if annotations:
        annotations = [
            Annotation(key=key, value=value) for key, value in annotations
        ]

    metadata = {}
    for k, v in json_utterance.items():
        if k not in (
            [
                _FIELD_UTTERANCE,
                _FIELD_PARTICIPANT,
                _FIELD_SLOT_VALUES,
                _FIELD_INTENT,
                _FIELD_DIALOGUE_ACTS,
                _FIELD_ANNOTATIONS,
            ]
        ):
            metadata[k] = v

    return AnnotatedUtterance(
        text=utterance_text,
        utterance_id=utterance_id,
        participant=participant,
        dialogue_acts=dialogue_acts,
        annotations=annotations,
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
        metadata = dialogue_data.get(_FIELD_METADATA, None)
        if metadata:
            dialogue._metadata = metadata

        for utterance_data in dialogue_data.get(_FIELD_CONVERSATION):
            annotated_utterance = json_to_annotated_utterance(utterance_data)
            dialogue.add_utterance(annotated_utterance)
            utterance_feedback = utterance_data.get(
                _FIELD_UTTERANCE_FEEDBACK, None
            )
            if utterance_feedback is not None:
                dialogue.add_utterance_feedback(
                    UtteranceFeedback(
                        utterance_id=annotated_utterance.utterance_id,
                        feedback=(
                            BinaryFeedback.POSITIVE
                            if utterance_feedback == 1
                            else BinaryFeedback.NEGATIVE
                        ),
                    ),
                    annotated_utterance.utterance_id,
                )
        dialogues.append(dialogue)

    return dialogues
