"""Extract user response utterance templates from annotated training data."""

from collections import defaultdict
import os
import json
from typing import Dict, List, Text
from dialoguekit.core.intent import Intent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance


def replace_slot_with_placeholder(utterance: str, slot_values: List) -> str:
    """Replaces the slot values with place holder.

    Args:
        utterance: User utterance in string, e.g.,
            I like action or fantasy movies.
        slot_values: Slot values in List, e.g.,
            [['GENRE','action'],['GENRE','fantasy']].

    Returns:
        User response template with slot replaced by placeholder,
        e.g., I like {GENRE} or {GENRE} movies.
    """
    for slot in slot_values:
        placeholder_label, value = slot
        utterance = utterance.replace(value, f"{{{placeholder_label}}}")
    return utterance


def extract_utterance_template(annotated_dialogue_file: str) -> Dict[str, List]:
    """Extracts utterance templates for each intent.

    Args:
        Annotated_dialog_file: annotated dialogue json file.

    Returns:
        A dictionary with user_intents and keys and a list of templates as
        values, e.g., {user_intent: [template...]}
    """
    if not os.path.isfile(annotated_dialogue_file):
        raise FileNotFoundError(
            f"Annotated dialog file not found: {annotated_dialogue_file}"
        )

    response_templates = dict()
    with open(annotated_dialogue_file) as input_file:
        annotated_dialogs = json.load(input_file)
        for dialog in annotated_dialogs:
            for utterance_record in dialog.get("conversation"):
                if (
                    utterance_record.get("participant") != "USER"
                ):  # Only use user utterance.
                    continue
                if utterance_record.get("intent") not in response_templates:
                    response_templates[utterance_record.get("intent")] = list()
                # Keep the original utterance as template when it does not
                # contain slot values.
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
                else:
                    # Extract response template via replacing slot values with
                    # placeholders.
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


def build_template_from_instances(
    utterances: List[AnnotatedUtterance],
) -> Dict[Text, List[Text]]:
    """Builds the NLG template.

    The Intent the Utterance comes with will be used. If no intent is present
    for an utterance it will be skipped.

    Args:
        utterances : List of AnnotatedUtterance-s.

    Returns:
        Dict with intent (as string) and lists with corresponding
        utterances (strings).
    """

    template = defaultdict(list)
    for utterance in utterances:
        if isinstance(utterance.intent, Intent):
            template[utterance.intent.label].append(utterance.text)
        else:
            print(
                f'Utterance was skipped.\nUtterance "{utterance.text}", \
                    does not have an associated intent.'
            )

    template = {
        intent: list(set(utterance)) for intent, utterance in template.items()
    }
    return template
