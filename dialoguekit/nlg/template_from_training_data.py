"""Extract user response utterance templates from annotated training data."""

import copy
import json
import os
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Set, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.intent import Intent
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation
from dialoguekit.nlu.models.satisfaction_classifier import (
    SatisfactionClassifier,
)
from dialoguekit.participant.participant import DialogueParticipant
from dialoguekit.utils.dialogue_reader import (
    _FIELD_ANNOTATIONS,
    _FIELD_CONVERSATION,
    _FIELD_DIALOGUE_ACTS,
    _FIELD_INTENT,
    _FIELD_PARTICIPANT,
    _FIELD_SLOT_VALUES,
    _FIELD_UTTERANCE,
)

# The default satisfaction level used for classifying the NLG template.
_DEFAULT_SATISFACTION = 3


def _replace_slot_with_placeholder(
    annotated_utterance: AnnotatedUtterance,
) -> None:
    """Replaces the slot values for all types of annotation with placeholders.

    Args:
        annotated_utterance: Utterance to modify.
    """
    annotations = annotated_utterance.annotations
    for annotation in annotations:
        placeholder_label, value = annotation.key, annotation.value
        annotated_utterance.text = annotated_utterance.text.replace(
            value, f"{{{placeholder_label}}}", 1
        )
        annotation.value = None

    dialogue_acts = annotated_utterance.dialogue_acts
    for da in dialogue_acts:
        for annotation in da.annotations:
            placeholder_label, value = annotation.slot, annotation.value
            annotated_utterance.text = annotated_utterance.text.replace(
                value, f"{{{placeholder_label}}}", 1
            )
            annotation.value = None


def build_template_from_instances(
    utterances: List[AnnotatedUtterance],
) -> Dict[str, List[AnnotatedUtterance]]:
    """Builds the NLG template.

    The dialogue acts from the utterances will be used to build the templates.
    If an utterance has multiple dialogue acts, the intents will be concatenated
    with a semicolon. If an utterance does not have any dialogue acts, it will
    be skipped.

    Args:
        utterances : List of utterances to build the template from.

    Returns:
        Dictionary with intents as keys and lists of corresponding templates.
    """
    template = defaultdict(list)
    for utterance in utterances:
        if utterance.dialogue_acts:
            _replace_slot_with_placeholder(utterance)
            intents = ";".join(
                [intent.label for intent in utterance.get_intents()]
            )
            template[intents].append(utterance)
        else:
            print(
                f'Utterance was skipped.\nUtterance "{utterance.text}", \
                    does not have an associated dialogue act.'
            )

    return_template = {
        intents: list(set(utterance)) for intents, utterance in template.items()
    }
    return return_template


def extract_utterance_template(  # noqa: C901
    annotated_dialogue_file: str,
    participant_to_learn: str = "USER",
    satisfaction_classifier: Optional[
        Union[None, SatisfactionClassifier]
    ] = None,
) -> Dict[str, List[AnnotatedUtterance]]:
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
        annotated_dialog_file: Annotated dialogue json file.
        participant_to_learn: Which participant we want to create a template on.
        satisfaction_classifier: SatisfactionClassifier.

    Returns:
        Dictionary with intents as keys and lists of corresponding templates.
    """
    if not os.path.isfile(annotated_dialogue_file):
        raise FileNotFoundError(
            f"Annotated dialog file not found: {annotated_dialogue_file}"
        )
    response_templates: DefaultDict[str, Set[AnnotatedUtterance]] = defaultdict(
        set
    )
    with open(annotated_dialogue_file, encoding="utf-8") as input_file:
        annotated_dialogs = json.load(input_file)
        for dialog in annotated_dialogs:
            counter_participant_utterance = None
            participant_utterance = None
            satisfaction = None
            for utterance_record in dialog.get(_FIELD_CONVERSATION):
                participant = utterance_record.get(_FIELD_PARTICIPANT)

                dialogue_acts = []
                for da in utterance_record.get(_FIELD_DIALOGUE_ACTS, []):
                    intent = (
                        Intent(da.get(_FIELD_INTENT, None))
                        if da.get(_FIELD_INTENT, None)
                        else None
                    )
                    slot_value_pairs = da.get(_FIELD_SLOT_VALUES, [])
                    if slot_value_pairs:
                        slot_value_pairs = [
                            SlotValueAnnotation(slot, value, start, end)
                            for slot, value, start, end in slot_value_pairs
                        ]
                    dialogue_acts.append(
                        DialogueAct(intent=intent, annotations=slot_value_pairs)
                    )
                if satisfaction_classifier:
                    annotated_utterance = AnnotatedUtterance(
                        text=utterance_record.get(_FIELD_UTTERANCE).strip(),
                        dialogue_acts=dialogue_acts,
                        metadata={
                            "satisfaction": _DEFAULT_SATISFACTION
                        },  # Satisfaction defaults to 3 (Normal)
                        participant=DialogueParticipant.AGENT,
                    )
                else:
                    annotated_utterance = AnnotatedUtterance(
                        text=utterance_record.get(_FIELD_UTTERANCE).strip(),
                        dialogue_acts=dialogue_acts,
                        participant=DialogueParticipant.AGENT,
                    )
                annotated_utterance_copy = copy.deepcopy(annotated_utterance)

                # Only use the utterances from the wanted participant
                if participant == participant_to_learn:
                    if (
                        counter_participant_utterance
                        and participant_utterance
                        and satisfaction_classifier
                    ):
                        annotated_utterance.metadata[
                            "satisfaction"
                        ] = satisfaction
                        counter_participant_utterance = None
                        participant_utterance = None

                    # Keep the original utterance as template when it does not
                    # contain slot values.
                    if "annotations" in utterance_record:
                        for slot, value in utterance_record.get(
                            _FIELD_ANNOTATIONS
                        ):
                            annotated_utterance.add_annotations(
                                [Annotation(slot, value)]
                            )
                    if satisfaction_classifier:
                        annotated_utterance_copy = copy.deepcopy(
                            annotated_utterance
                        )
                    _replace_slot_with_placeholder(annotated_utterance)
                    intents = ";".join(
                        [
                            intent.label
                            for intent in annotated_utterance.get_intents()
                        ]
                    )
                    response_templates[intents].add(annotated_utterance)
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

    return_template = {
        key: list(val) for key, val in response_templates.items()
    }
    return return_template
