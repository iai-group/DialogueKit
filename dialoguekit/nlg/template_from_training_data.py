"""Extract user response utterance templates from annotated training data."""

from collections import defaultdict
import os
import json
import re
import copy
from typing import Dict, List, Union
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.nlu.models.satisfaction_classifier import (
    SatisfactionClassifier,
)


def _replace_slot_with_placeholder(
    annotated_utterance: AnnotatedUtterance,
) -> None:
    annotations = annotated_utterance.get_annotations()
    for annotation in annotations:
        placeholder_label, value = annotation.slot, annotation.value
        annotated_utterance._text = annotated_utterance.text.replace(
            value, f"{{{placeholder_label}}}", 1
        )
        annotation._value = ""


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
    participant_to_learn: str = "USER",
    satisfaction_classifier: Union[None, SatisfactionClassifier] = None,
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
            counter_participant_utterance = None
            participant_utterance = None
            satisfaction = None
            for utterance_record in dialog.get("conversation"):
                participant = utterance_record.get("participant")
                annotated_utterance = AnnotatedUtterance(
                    text=utterance_record.get("utterance").strip(),
                    intent=Intent(utterance_record.get("intent")),
                    satisfaction=3,  # Satisfaction defaults to 3 (Normal)
                )
                annotated_utterance_copy = copy.deepcopy(annotated_utterance)

                # Only use the utterances from the wanted participant
                if participant == participant_to_learn:
                    if (
                        counter_participant_utterance
                        and participant_utterance
                        and satisfaction_classifier
                    ):
                        annotated_utterance._satisfaction = satisfaction
                        counter_participant_utterance = None
                        participant_utterance = None

                    # Keep the original utterance as template when it does not
                    # contain slot values.
                    if "slot_values" in utterance_record:
                        for slot, value in utterance_record.get("slot_values"):
                            annotated_utterance.add_annotation(
                                Annotation(slot=slot, value=value)
                            )
                        if satisfaction_classifier:
                            annotated_utterance_copy = copy.deepcopy(
                                annotated_utterance
                            )

                        _replace_slot_with_placeholder(annotated_utterance)

                    response_templates[annotated_utterance.intent].add(
                        annotated_utterance
                    )
                    participant_utterance = annotated_utterance_copy
                else:
                    if participant_utterance and satisfaction_classifier:
                        satisfaction = satisfaction_classifier.classify_text(
                            dialogue_text=(
                                f"{participant_utterance.text} "
                                f"{annotated_utterance_copy.text}"
                            )
                        )
                        counter_participant_utterance = annotated_utterance_copy

    response_templates = {
        key: list(val) for key, val in response_templates.items()
    }
    return response_templates


def generate_cooperativeness_measure(
    template: Dict[Intent, List[AnnotatedUtterance]], annotation_bonus: int = 2
) -> Dict[Intent, List[AnnotatedUtterance]]:
    """Generates a cooperativness score for every annotated utterance.

    The cooperativness score is a normalized length measure for every Intent.
    Annotations get boosted with annotation_bonus. This bonus gets added for
    every Annotation the Utterance contains.

    Note:
        This method does the generation innplace, but also returns the same
        object.

    Args:
        template: Template file from extract_utterance_template() or
                    build_template_from_instances().
        annotation_bonus: Bonus value for every Annotation the Utterance
                    contains.

    Returns:
        The same template that got passed as an argument, but now cooperativness
        has been added to the AnnotatedUtterances.
    """
    annotation_expression = r"{.*?}"
    for _, annotated_utterances in template.items():

        max_score = 0
        for annotated_utterance in annotated_utterances:
            word_score = len(annotated_utterance.text.split(" "))
            annotations_found = re.findall(
                pattern=annotation_expression, string=annotated_utterance.text
            )
            if annotations_found:
                word_score = (
                    word_score + len(annotations_found) * annotation_bonus
                )

            annotated_utterance._cooperativeness = word_score
            if word_score > max_score:
                max_score = word_score

        for annotated_utterance in annotated_utterances:
            annotated_utterance._cooperativeness = (
                annotated_utterance.cooperativeness / max_score
            )
    return template
