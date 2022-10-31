"""NLG component."""
import json
import random
import sys
from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.nlg.nlg_abstract import AbstractNLG
from dialoguekit.participant.participant import DialogueParticipant


class TemplateNLG(AbstractNLG):
    def __init__(
        self, response_templates: Dict[Intent, List[AnnotatedUtterance]]
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
        intent: Intent,
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
            intent: The intent of the wanted Utterance.
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

        templates = self._response_templates.get(intent)

        # If desired 'intent' is not in the template, use fallback.
        if templates is None:
            return AnnotatedUtterance(
                intent=intent,
                text="Sorry, I did not understand you.",
                participant=DialogueParticipant.AGENT,
            )
        templates = self._filter_templates(
            templates=templates,
            annotations=annotations,
            force_annotation=force_annotation,
        )
        # Check if filtering has filtered out everything
        if len(templates) == 0:
            raise ValueError("NLG text generation failed.")

        response_utterance = random.choice(templates)
        response_utterance = deepcopy(response_utterance)

        # Clear out annotations
        response_utterance._annotations = []

        if annotations is not None:
            for annotation in annotations:
                response_utterance._text = response_utterance._text.replace(
                    f"{{{annotation.slot}}}", annotation.value, 1
                )
                response_utterance.add_annotation(annotation)
        return response_utterance

    def dump_template(self, filepath: str) -> None:
        """Dump template to JSON."""
        dump_dict = {}
        for intent, utterances in self._response_templates.items():
            dump_dict[intent.label] = [
                annotated_utterance.text for annotated_utterance in utterances
            ]

        with open(filepath, "w") as file:
            json.dump(dump_dict, file, indent=4)

    def _filter_templates(
        self,
        templates: List[AnnotatedUtterance],
        annotations: List[Annotation],
        force_annotation: bool,
    ) -> List[AnnotatedUtterance]:
        """Filters available templates based on annotations.

        The list of annotations is used to filter the templates in such a way,
        that only the templates that are possible to instantiate given these
        annotations are returned.
        If a template does not contain any annotations it will remain in the
        list of available templates. Templates that do not contain any
        annotations will not be removed, as long as 'force_annotations' is set
        to False. If its 'True' these will also be filtered out.

        Args:
            templates: Template annotated utterance.
            annotations: List of annotations to be used for filtering.
            force_annotation: If 'True' and annotations are provided templates
                without annotations will also be filtered out.

        Returns:
            List of annotated utterances that are possible to create with the
            provided annotations.
        """
        filtered_annotated_utterances = []
        annotations_slots = set([annotation.slot for annotation in annotations])
        for annotated_utterance in templates:
            utterance_slots = set(
                [
                    annotation.slot
                    for annotation in annotated_utterance.get_annotations()
                ]
            )
            if all(x in annotations_slots for x in utterance_slots):
                filtered_annotated_utterances.append(annotated_utterance)
        if force_annotation and len(annotations) > 0:
            filtered_annotated_utterances = [
                template
                for template in filtered_annotated_utterances
                if len(template.get_annotations()) > 0
            ]
        return filtered_annotated_utterances

    def get_intent_annotation_specifications(
        self,
        intent: Intent,
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
            intent (Intent): Intent of the desired responses.

        Returns:
            List[Annotation]: _description_
        """
        templates = self._response_templates.get(intent)
        if templates is None:
            raise TypeError(f"Intent: {intent}, is not part of the template")

        min_annotations = {"amount": sys.maxsize, "examples": []}
        max_annotations = {"amount": 0, "examples": []}

        template_lengths = [
            len(template.get_annotations()) for template in templates
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
