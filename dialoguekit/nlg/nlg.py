import random
from typing import List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent

from dialoguekit.nlg.template_from_training_data import (
    extract_utterance_template_typed,
)


class NLG:
    """Represents a Natural Language Generation (NLG) component."""

    def __init__(self, template_file: str) -> None:
        """Initializes the NLG component."""
        self.__response_templates_typed = extract_utterance_template_typed(
            template_file
        )

    def generate_utterance_text_typed(
        self, intent: Intent, annotations: List[Annotation]
    ) -> AnnotatedUtterance:
        """Turns a structured utterance into a textual one.

        Args:
            intent: intent label string.
            slot values: slot value dict, e.g. {"GENRE": "action"}.

        Returns:
            generated response text using templates.
        """
        # Todo: match the needed slots with the template
        templates = self.__response_templates_typed.get(intent)
        response_utterance = random.choice(templates)
        for annotation in annotations:
            response_utterance._text = response_utterance._text.replace(
                "{" + annotation.slot + "}", annotation.value
            )
            response_utterance.add_annotation(annotation)
        return response_utterance
