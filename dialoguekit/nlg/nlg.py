import random
from typing import List
from copy import copy
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlg.template_from_training_data import (
    extract_utterance_template,
    build_template_from_instances,
)


class NLG:
    """Represents a Natural Language Generation (NLG) component."""

    def __init__(self) -> None:
        """Initializes the NLG component."""
        self.__response_templates = None

    def template_from_file(self, template_file: str) -> None:
        """Generates template from moviebot JSON format."""
        self.__response_templates = extract_utterance_template(template_file)

    def template_from_objects(
        self, utterances: List[AnnotatedUtterance]
    ) -> None:
        """Generates template from instances."""
        self.__response_templates = build_template_from_instances(
            utterances=utterances
        )

    def generate_utterance_text(
        self, intent: Intent, annotations: List[Annotation]
    ) -> AnnotatedUtterance:
        """Turns a structured utterance into a textual one.

        Args:
            intent: The intent of the wanted Utterance.
            annotations: The wanted annotations in the respone Utterance.

        Returns:
            Generated response utterance using templates.
        """
        if self.__response_templates is None:
            raise ValueError(
                "The template is not generated, use of of the\
                template_from methods"
            )

        # Todo: match the needed slots with the template
        templates = self.__response_templates.get(intent)
        response_utterance = random.choice(templates)
        response_utterance = copy(response_utterance)
        for annotation in annotations:
            response_utterance._text = response_utterance._text.replace(
                f"{{{annotation.slot}}}", annotation.value, 1
            )
            response_utterance.add_annotation(annotation)
        return response_utterance
