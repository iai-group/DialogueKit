import random
from typing import List, Optional, Union, Dict
from copy import deepcopy
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.models.satisfaction_classifier import (
    SatisfactionClassifier,
)
from dialoguekit.nlg.template_from_training_data import (
    extract_utterance_template,
    build_template_from_instances,
    generate_cooperativeness_measure,
)


class NLG:
    """Represents a Natural Language Generation (NLG) component."""

    def __init__(self) -> None:
        """Initializes the NLG component."""
        self._response_templates = None
        self._GENERATED_SATISFACTION = False

    def template_from_file(
        self,
        template_file: str,
        participant_to_learn: str = "USER",
        satisfaction_classifier: Union[None, SatisfactionClassifier] = None,
    ) -> None:
        """Generates template from IAI MovieBot JSON format."""
        self._response_templates = extract_utterance_template(
            annotated_dialogue_file=template_file,
            participant_to_learn=participant_to_learn,
            satisfaction_classifier=satisfaction_classifier,
        )
        if satisfaction_classifier:
            self._GENERATED_SATISFACTION = True

    def template_from_objects(
        self, utterances: List[AnnotatedUtterance]
    ) -> None:
        """Generates template from instances."""
        self._response_templates = build_template_from_instances(
            utterances=utterances
        )

    def generate_cooperativness(self):
        if self._response_templates is None:
            raise TypeError(
                "You need to run one of the template_from_*() functions, \
                    before running this method."
            )
        generate_cooperativeness_measure(self._response_templates)

    def generate_utterance_text(
        self,
        intent: Intent,
        annotations: Optional[Union[List[Annotation], None]] = None,
        cooperativeness: Optional[Union[float, None]] = None,
        satisfaction: Optional[Union[float, None]] = None,
        force_annotation: Optional[bool] = False,
    ) -> Union[AnnotatedUtterance, bool]:
        """Turns a structured utterance into a textual one.

        Generating a response is a multi-step process.
            1. Responses to the desired 'intent' will be selected.
            2. Based on the list of 'annotations' only the possible responses,
                are kept. e.g. Filter out responses that are not possible to
                use are removed.
            3. If 'satisfaction' is provided:
                Filter to the closest responses that are possible, and select a
                random one.
            3. If 'satisfaction' is not provided:
                Select a random one without looking at the satisfaction metric.

        Args:
            intent: The intent of the wanted Utterance
            annotations: The wanted annotations in the response Utterance
            satisfaction: Desired satisfaction score of the response.
            force_annotation: if 'True' and 'annotations' are provided,
                                responses without annotations will also be
                                filtered out during step 2.

        Returns:
            Generated response utterance using templates.
            Note: if the filtering after step 1 and 2 does not find any response
            that satisfies the criteria 'False' will be returned.
        """
        if self._response_templates is None:
            raise ValueError(
                "The template is not generated, use of of the\
                template_from methods"
            )
        if annotations is None:
            annotations = []

        templates = self._response_templates.get(intent)
        templates = self._filter_templates(
            templates=templates,
            annotations=annotations,
            force_annotation=force_annotation,
        )
        # Check if filtering has filtered out everything
        if len(templates) == 0:
            return False

        if cooperativeness is not None:
            response_utterance = self._select_closest_to_cooperativness(
                templates, cooperativeness
            )

        if satisfaction is not None:
            response_utterance = self._select_closest_to_satisfaction(
                templates, satisfaction
            )

        if cooperativeness is None and satisfaction is None:
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

    def _filter_templates(
        self,
        templates: List[AnnotatedUtterance],
        annotations: List[Annotation],
        force_annotation: bool,
    ) -> List[AnnotatedUtterance]:
        """Filters available templates based on annotations.

        The list of annotations is used to filter the templates in such a way,
        that only the templates that are possible to create are returned.
        If a template does not contain any annotations it will remain in the
        list of available templates. As long as 'force_annotations' is False.
        If its 'True' these will also be filtered out.

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

    def _select_closest_to_satisfaction(
        self, templates: List[AnnotatedUtterance], satisfaction: int
    ):
        """Find the closest annotated utterance based on satisfaction.

        If there are multiple possible options a random one will be selected.

        Args:
            templates: AnnotatedUtterances with satisfaction metric.
            satisfaction: The desired satisfaction score.

        Returns:
            AnnotatedUtterance that has the closest satisfaction score.
        """
        templates = sorted(templates, key=lambda item: item.satisfaction)

        closest_under = templates[0]
        closest_over = templates[-1]
        response_utterance = []
        for annotated_utterance in templates:
            if annotated_utterance.satisfaction == satisfaction:
                response_utterance.append(annotated_utterance)
                break
            if annotated_utterance.satisfaction < satisfaction:
                closest_under = annotated_utterance
            if annotated_utterance.satisfaction > satisfaction:
                closest_over = annotated_utterance
                break

        if len(response_utterance) == 0:
            distance_down = abs(closest_under.satisfaction - satisfaction)
            distance_up = abs(closest_over.satisfaction - satisfaction)
            if distance_down <= distance_up:
                closest_under = [
                    template
                    for template in templates
                    if template.satisfaction == closest_under.satisfaction
                ]
                response_utterance.extend(closest_under)
            else:
                closest_over = [
                    template
                    for template in templates
                    if template.satisfaction == closest_over.satisfaction
                ]
                response_utterance.extend(closest_over)

        return deepcopy(random.choice(response_utterance))

    def _select_closest_to_cooperativness(
        self, templates: List[AnnotatedUtterance], cooperativeness: float
    ):
        """Find the closest annotated utterance based on cooperativness

        Args:
            templates: AnnotatedUtterance with cooperativness.
            cooperativeness (float): The desired cooperativness score.

        Returns:
            AnnotatedUtterance with that has the closest cooperativness score.
        """
        templates = sorted(templates, key=lambda item: item.cooperativeness)

        closest_under = templates[0]
        closest_over = templates[-1]
        response_utterance = None
        for annotated_utterance in templates:
            if annotated_utterance.cooperativeness == cooperativeness:
                response_utterance = deepcopy(annotated_utterance)
                break
            if annotated_utterance.cooperativeness < cooperativeness:
                closest_under = annotated_utterance
            if annotated_utterance.cooperativeness > cooperativeness:
                closest_over = annotated_utterance
                break

        if response_utterance is None:
            distance_down = abs(closest_under.cooperativeness - cooperativeness)
            distance_up = abs(closest_over.cooperativeness - cooperativeness)
            if distance_down <= distance_up:
                response_utterance = deepcopy(closest_under)
            else:
                response_utterance = deepcopy(closest_over)

        return response_utterance

    def get_intent_annotation_specifications(
        self,
        intent: Intent,
    ) -> Dict[str, Dict[str, Union[int, List[AnnotatedUtterance]]]]:
        """Returns dictionary with the min and max annotated utterances.

        The dictionary is structured as such:
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

        This is useful if you want to look into which options the nlg has for a
        specific Intent and which annotations are needed.

        Args:
            intent (Intent): Intent of the desired responses.

        Returns:
            List[Annotation]: _description_
        """
        templates = self._response_templates.get(intent)
        if templates is None:
            raise TypeError(f"Intent: {intent}, is not part of the template")

        min_annotations = {"amount": 1000, "examples": []}
        max_annotations = {"amount": 0, "examples": []}
        for template in templates:
            if len(template.get_annotations()) > max_annotations.get("amount"):
                max_annotations["amount"] = len(template.get_annotations())
                max_annotations["examples"].append(template)
            if len(template.get_annotations()) < min_annotations.get("amount"):
                min_annotations["amount"] = len(template.get_annotations())
                min_annotations["examples"].append(template)

            if len(template.get_annotations()) == max_annotations.get("amount"):
                max_annotations["examples"].append(template)
            if len(template.get_annotations()) == min_annotations.get("amount"):
                min_annotations["examples"].append(template)

        return {"min": min_annotations, "max": max_annotations}
