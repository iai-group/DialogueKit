"""Extract user response utterance templates from annotated training data."""

from collections import defaultdict
import os
import json
from typing import Dict, List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance


def _replace_slot_with_placeholder(
    annotated_utterance: AnnotatedUtterance,
) -> None:
    annotations = annotated_utterance.get_annotations()
    for annotation in annotations:
        placeholder_label, value = annotation.slot, annotation.value
        annotated_utterance._text = annotated_utterance.text.replace(
            value, f"{{{placeholder_label}}}"
        )
        annotated_utterance._annotations = []


def build_template_from_instances(
    utterances: List[AnnotatedUtterance],
) -> Dict[Intent, List[AnnotatedUtterance]]:
    """Builds the NLG template.

    The Intent the Utterance comes with will be used. If no intent is present
    for an utterance it will be skipped.

    Args:
        utterances : List of AnnotatedUtterance-s.

    Returns:
        Dict with Intents and lists with corresponding AnnotatedUtterances.
    """

    template = defaultdict(list)
    for utterance in utterances:
        if isinstance(utterance.intent, Intent):
            _replace_slot_with_placeholder(utterance)
            template[utterance.intent].append(utterance)
        else:
            print(
                f'Utterance was skipped.\nUtterance "{utterance.text}", \
                    does not have an associated intent.'
            )

    template = {
        intent: list(set(utterance)) for intent, utterance in template.items()
    }
    return template


def extract_utterance_template(
    annotated_dialogue_file: str,
) -> Dict[Intent, List[AnnotatedUtterance]]:
    """Extracts utterance templates for each intent.

    Args:
        Annotated_dialog_file: annotated dialogue json file.

    Returns:
        Dict with Intents and lists with corresponding AnnotatedUtterances.
    """
    if not os.path.isfile(annotated_dialogue_file):
        raise FileNotFoundError(
            f"Annotated dialog file not found: {annotated_dialogue_file}"
        )

    response_templates = defaultdict(set)
    with open(annotated_dialogue_file) as input_file:
        annotated_dialogs = json.load(input_file)
        for dialog in annotated_dialogs:
            for utterance_record in dialog.get("conversation"):
                participant = utterance_record.get("participant")
                annotated_utterance = AnnotatedUtterance(
                    text=utterance_record.get("utterance").strip(),
                    intent=Intent(utterance_record.get("intent")),
                )
                if participant != "USER":  # Only use user utterance.
                    continue

                # Keep the original utterance as template when it does not
                # contain slot values.
                if "slot_values" in utterance_record:
                    for slot, value in utterance_record.get("slot_values"):
                        annotated_utterance.add_annotation(
                            Annotation(slot=slot, value=value)
                        )
                    _replace_slot_with_placeholder(annotated_utterance)
                response_templates[annotated_utterance.intent].add(
                    annotated_utterance
                )
    response_templates = {
        key: list(val) for key, val in response_templates.items()
    }
    return response_templates
