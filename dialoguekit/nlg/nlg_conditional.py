import random
from collections import defaultdict
from copy import deepcopy
from numbers import Number
from typing import Dict, List, Optional, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.nlg.nlg import NLG
from dialoguekit.participant.participant import DialogueParticipant


class ConditionalNLG(NLG):
    def __init__(
        self, response_templates: Dict[Intent, List[AnnotatedUtterance]]
    ) -> None:
        """Template based NLG with support for conditional.

        The conditional field has to be part of the AnnotatedUtterance metadata
        field and also a Number.
        """
        super().__init__(response_templates=response_templates)

    def generate_utterance_text(
        self,
        intent: Intent,
        annotations: Optional[Union[List[Annotation], None]] = None,
        conditional: Optional[Union[str, None]] = None,
        conditional_value: Optional[Union[Number, None]] = None,
        force_annotation: Optional[bool] = False,
    ) -> Union[AnnotatedUtterance, bool]:
        """Turns a structured utterance into a textual one.

        Note:
        If the template does not contain the desired intent, a fallback will be
        used. Stating "Sorry, I did not understand you." The response will have
        the same 'intent'.

        Generating a response is a multi-step process.
            1. Responses to the desired 'intent' will be selected.
            2. Based on the list of 'annotations' only the possible responses,
                are kept. e.g. Filter out responses that are not possible to
                use are removed.
            3. If conditional is provided:
                Filter to the closest responses that are possible to the
                conditional_value, and select a random one.
            3. If conditional is not provided:
                Select a random one without looking at the conditional_value.

        Args:
            intent: The intent of the wanted Utterance
            annotations: The wanted annotations in the response Utterance
            conditional: The desired metadata field to use as a conditional.
            conditional_value: The desired conditional value score.
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
            return False

        if conditional is not None:
            response_utterance = self._select_closest_to_conditional(
                templates=templates,
                conditional=conditional,
                conditional_value=conditional_value,
            )
        else:
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

    def _select_closest_to_conditional(
        self,
        templates: List[AnnotatedUtterance],
        conditional: str,
        conditional_value: Number,
    ) -> AnnotatedUtterance:
        """Find the closest annotated utterance based on conditional.

        If there are multiple possible options a random one will be selected.

        Args:
            templates: AnnotatedUtterances with conditional in the metadata
            conditional: The desired metadata field to use as a conditional.
            conditional_value: The desired conditional value score.

        Returns:
            AnnotatedUtterance that has the closest conditional value.
        """
        templates = sorted(
            templates, key=lambda item: item.metadata.get(conditional)
        )

        distances = defaultdict(list)
        for annotated_utterance in templates:
            dist = abs(
                annotated_utterance.metadata.get(conditional)
                - conditional_value
            )
            distances[dist].append(annotated_utterance)

        lowest_distance = sorted(list(distances.keys()))[0]
        return deepcopy(random.choice(distances[lowest_distance]))
