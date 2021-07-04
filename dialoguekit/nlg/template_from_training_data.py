"""Extract user response utterance templates from annotated training data."""

import os
import json
from typing import Dict


def replace_slot_with_placeholder(utterance: str, slot_values: str) -> str:
    """Replaces the slot values with place holder.

    Args:
        Utterance: user utterance in string, e.g., I like action or fantasy movies.
        Slot_values: slot values in string, e.g., 'GENRE:action;GENRE:fantasy'.

    Returns:
        User response template with slot replaced by placeholder, e.g., I like {GENER} or {GENER} movies.
    """
    for slot in slot_values.split(";"):
        placeholder_label, value = slot.split(":")
        utterance = utterance.replace(value, "{" + placeholder_label + "}")
    return utterance


def extract_utterance_template(annotated_dialog_file) -> Dict:
    """Extracts utterance template for each intent.

    Args:
        Annotated_dialog_file: annotated dialogue json file.

    Returns:
        Response template: {user_intent: [template...]}
    """
    if not os.path.isfile(annotated_dialog_file):
        raise FileNotFoundError(
            f"Annotated dialog file not found: {annotated_dialog_file}"
        )

    response_templates = dict()
    with open(annotated_dialog_file) as input_file:
        annotated_dialogs = json.load(input_file)
        for dialog in annotated_dialogs:
            for utterance_record in dialog.get("conversation"):
                if (
                    utterance_record.get("participant") != "USER"
                ):  # Only use user utterance.
                    continue
                if utterance_record.get("intent") not in response_templates:
                    response_templates[utterance_record.get("intent")] = list()
                # Keep the original utterance as template when it does not contain slot values.
                if "slot_values" not in utterance_record:
                    if (
                        utterance_record.get("utterance")
                        not in response_templates[
                            utterance_record.get("intent")
                        ]
                    ):
                        response_templates[
                            utterance_record.get("intent")
                        ].append(utterance_record.get("utterance"))
                else:  # Extract response template via replacing slot values with placeholders.
                    extracted_template = replace_slot_with_placeholder(
                        utterance_record.get("utterance"),
                        utterance_record.get("slot_values"),
                    )
                    if (
                        extracted_template
                        not in response_templates[
                            utterance_record.get("intent")
                        ]
                    ):
                        response_templates[
                            utterance_record.get("intent")
                        ].append(extracted_template)
    return response_templates
