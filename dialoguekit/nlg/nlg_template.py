"""NLG component."""

import json
import random
import sys
from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.nlg.nlg_abstract import AbstractNLG
from dialoguekit.participant.participant import DialogueParticipant


class TemplateNLG(AbstractNLG):
    def __init__(
        self, response_templates: Dict[str, List[AnnotatedUtterance]]
    ) -> None:
        """Template-based NLG.

        To use this NLG component, one of the template extraction methods from
        `template_from_training_data.py` has to be used.

        Args:
            response_templates: Response templates for NLG.
        """
        self._response_templates = response_templates

    def generate_utterance_text(
        self,
        dialogue_acts: List[DialogueAct],
        annotations: Optional[Union[List[Annotation], None]] = None,
        force_annotation: Optional[bool] = False,
    ) -> AnnotatedUtterance:
        """Turns a structured utterance into a textual one.

        .. note::

            If the template does not contain the desired intent, a fallback will
            be used. Stating "Sorry, I did not understand you." The response
            will have the same 'intent'.

        Generating a response is a multi-step process:

        1. Responses to the desired 'intent' will be selected.

        2. Based on the list of 'annotations', only the possible responses are
           kept, i.e., filter out responses that are not usable.

        3. If 'satisfaction' is provided:
           Filter to the closest responses that are possible, and select a
           random one.

        4. If 'satisfaction' is not provided:
           Select a random one without looking at the satisfaction metric.


        Args:
            dialogue_acts: The dialogue acts of the wanted Utterance.
            annotations: The wanted annotations in the response Utterance.
            force_annotation: if 'True' and 'annotations' are provided,
              responses without annotations will also be filtered out during
              step 2.

        Returns:
            Generated response utterance using templates.

            .. note::

                Note: if the filtering after step 1 and 2 does not find any
                response that satisfies the criteria 'ValueError' will be
                raised.
        """
        if self._response_templates is None:
            raise ValueError(
                "The template is not generated, use of of the\
                template_from methods"
            )

        if annotations is None:
            annotations = []

        templates = self._response_templates.get(
            ";".join([da.intent.label for da in dialogue_acts])
        )

        # If desired 'intent' is not in the template, use fallback.
        if templates is None:
            return AnnotatedUtterance(
                dialogue_acts=dialogue_acts,
                text="Sorry, I did not understand you.",
                participant=DialogueParticipant.AGENT,
            )

        templates = self._filter_templates(
            templates=templates,
            dialogue_acts=dialogue_acts,
            annotations=annotations,
            force_annotation=force_annotation,
        )
        # Check if filtering has filtered out everything
        if len(templates) == 0:
            raise ValueError("NLG text generation failed.")

        response_utterance = random.choice(templates)
        response_utterance = deepcopy(response_utterance)

        # Clear out dialogue acts and annotations
        response_utterance.dialogue_acts = []
        response_utterance.annotations = []

        # If annotations are provided, use them to fill in the template
        response_utterance = self._fill_template_with_annotations(
            response_utterance, dialogue_acts, annotations
        )
        return response_utterance

    def _fill_template_with_annotations(
        self,
        response_utterance: AnnotatedUtterance,
        dialogue_acts: List[DialogueAct],
        annotations: List[Annotation],
    ) -> AnnotatedUtterance:
        """Fills the template response based on provided annotations.

        Args:
            response_utterance: Template response.
            dialogue_acts: Dialogue acts with slot-value pairs for annotations.
            annotations: Annotations to fill the template with.

        Returns:
            Response template filled with annotations.
        """
        for da in dialogue_acts:
            if da.annotations:
                for da_annotation in da.annotations:
                    response_utterance.text = response_utterance.text.replace(
                        f"{{{da_annotation.slot}}}", da_annotation.value, 1
                    )
            response_utterance.add_dialogue_acts([da])

        for annotation in annotations:
            response_utterance.text = response_utterance.text.replace(
                f"{{{annotation.key}}}", annotation.value, 1
            )
            response_utterance.add_annotations([annotation])
        return response_utterance

    def dump_template(self, filepath: str) -> None:
        """Dump template to JSON."""
        dump_dict = {}
        for intents, utterances in self._response_templates.items():
            dump_dict[intents] = [
                annotated_utterance.text for annotated_utterance in utterances
            ]

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(dump_dict, file, indent=4)

    def _filter_templates(
        self,
        templates: List[AnnotatedUtterance],
        dialogue_acts: List[DialogueAct],
        annotations: List[Annotation],
        force_annotation: bool,
    ) -> List[AnnotatedUtterance]:
        """Filters available templates based on utterance's annotations.

        The list of annotations is used to filter the templates in such a way,
        that only the templates that are possible to instantiate given these
        annotations are returned.
        If a template does not contain any annotations it will remain in the
        list of available templates. Templates that do not contain any
        annotations will not be removed, as long as 'force_annotations' is set
        to False. If its 'True' these will also be filtered out.

        Args:
            templates: Template annotated utterance.
            dialogue_acts: List of dialogue acts to be used for filtering.
            annotations: List of annotations to be used for filtering.
            force_annotation: If 'True' and annotations are provided templates
                without annotations will also be filtered out.

        Returns:
            List of annotated utterances that are possible to create with the
            provided annotations.
        """
        filtered_annotated_utterances = []

        da_annotations_slots = set(
            [
                (da.intent, annotation.slot)
                for da in dialogue_acts
                if da.annotations
                for annotation in da.annotations
            ]
        )
        annotations_slots = set([annotation.key for annotation in annotations])

        for annotated_utterance in templates:
            utterance_da_slots = set(
                [
                    (da.intent, annotation.slot)
                    for da in annotated_utterance.dialogue_acts
                    if da.annotations
                    for annotation in da.annotations
                ]
            )
            utterance_slots = set(
                [
                    annotation.key
                    for annotation in annotated_utterance.annotations
                ]
            )
            if all(
                x in da_annotations_slots for x in utterance_da_slots
            ) and all(x in annotations_slots for x in utterance_slots):
                filtered_annotated_utterances.append(annotated_utterance)

        if force_annotation and (
            len([da for da in dialogue_acts if da.annotations]) > 0
            or len(annotations) > 0
        ):
            filtered_annotated_utterances = [
                template
                for template in filtered_annotated_utterances
                if template.num_dialogue_act_annotations() > 0
                or len(template.annotations) > 0
            ]
        return filtered_annotated_utterances

    def get_intent_annotation_specifications(
        self,
        dialogue_acts: List[DialogueAct],
    ) -> Dict[str, Dict[str, Any]]:
        """Returns dictionary with the min and max annotated utterances.

        The dictionary is structured as such:

        .. code:: python

            {
                "min":{
                    "amount": int
                    "examples": List[AnnotatedUtterance]
                }
                "max":{
                    "amount": int
                    "examples": List[AnnotatedUtterance]
                }
            }

        This is useful if you want to look into which options the NLG has for a
        specific Intent and which annotations are needed.

        Args:
            dialogue_acts: List of dialogue acts of the desired responses.

        Returns:
            List[Annotation]: _description_
        """
        templates = self._response_templates.get(
            ";".join([da.intent.label for da in dialogue_acts])
        )
        if templates is None:
            raise TypeError(
                f"Dialogue acts: {dialogue_acts}, are not part of the template"
            )

        min_annotations = {"amount": sys.maxsize, "examples": []}
        max_annotations = {"amount": 0, "examples": []}

        template_lengths = [
            template.num_dialogue_act_annotations() + len(template.annotations)
            for template in templates
        ]
        max_annotations["amount"] = max(template_lengths)
        min_annotations["amount"] = min(template_lengths)
        max_annotations["examples"] = [
            templates[i]
            for i, _ in enumerate(template_lengths)
            if template_lengths[i] == max_annotations["amount"]
        ]
        min_annotations["examples"] = [
            templates[i]
            for i, _ in enumerate(template_lengths)
            if template_lengths[i] == min_annotations["amount"]
        ]

        return {"min": min_annotations, "max": max_annotations}
