"""Extract user response utterance templates from annotated training data."""

from collections import defaultdict
import os
import json
import copy
from typing import Dict, List, Union, Optional
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.nlu.models.satisfaction_classifier import (
    SatisfactionClassifier,
)

# The default satisfaction level used for classifying the NLG template.
_DEFAULT_SATISFACTION = 3


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
    satisfaction_classifier: Optional[
        Union[None, SatisfactionClassifier]
    ] = None,
) -> Dict[Intent, List[AnnotatedUtterance]]:
    """Extracts utterance templates for each intent.

    If a Satisfaction Classifier is provided it will be used to classify the
    utterances. The classification logic is as follows:
        - Hold participant utterance.
        - Hold counter-participant utterance.
        - Concatenate participant and counter-participant utterance and
            classify satisfaction.
        - The next utterance from participant will be given the satisfaction
            from the concatenated utterance from the previous utterances.
            reflecting the satisfaction at that given point in time.

    Args:
        Annotated_dialog_file: annotated dialogue json file.
        participant_to_learn: Which participant we want to create a template on.
        satisfaction_classifier: SatisfactionClassifier

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
                    metadata={
                        satisfaction: _DEFAULT_SATISFACTION
                    },  # Satisfaction defaults to 3 (Normal)
                )
                annotated_utterance_copy = copy.deepcopy(annotated_utterance)

                # Only use the utterances from the wanted participant
                if participant == participant_to_learn:
                    if (
                        counter_participant_utterance
                        and participant_utterance
                        and satisfaction_classifier
                    ):
                        annotated_utterance._metadata[
                            "satisfaction"
                        ] = satisfaction
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
