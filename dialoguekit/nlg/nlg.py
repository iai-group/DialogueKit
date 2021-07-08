import random
from typing import Dict

from dialoguekit.nlg.template_from_training_data import extract_utterance_template


class NLG:
    """Represents a Natural Language Generation (NLG) component."""

    def __init__(self, template_file: str) -> None:
        """Initializes the NLG component."""
        self.__response_templates = extract_utterance_template(template_file)

    def generate_utterance_text(self, intent: str, slot_values: Dict) -> str:
        """Turns a structured utterance into a textual one.

        Args:
            intent: intent label string.
            slot values: slot value dict, e.g. {"GENRE": "action"}.

        Returns:
            generated response text using templates.
        """
        # Todo: match the needed slots with the template
        templates = self.__response_templates.get(intent)
        response_text = random.choice(templates)
        for placeholder, value in slot_values.items():
            response_text = response_text.replace("{"+placeholder+"}", value)
        return response_text
