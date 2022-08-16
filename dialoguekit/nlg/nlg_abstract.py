"""Abstract interface for NLG."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent


class NLG(ABC):
    def __init__(self) -> None:
        """Represents a Natural Language Generation (NLG) component."""
        self._response_templates: Dict[
            Intent, List[AnnotatedUtterance]
        ] = dict()
        self._GENERATED_SATISFACTION: bool = False

    @abstractmethod
    def template_from_file(
        self,
        template_file: str,
        participant_to_learn: str = "USER",
    ) -> None:
        """Generates template from DialogueKit JSON format.

        Args:
            template_file: Path to the template file containing annotated
              dialogues.
            participant_to_learn: Defines which participant from the dialogues
              to consider utterances for.
            satisfaction_classifier: TBD.
        """
        pass

    @abstractmethod
    def template_from_objects(
        self,
        utterances: List[AnnotatedUtterance],
    ) -> None:
        """Generates template from a list of annotated utterances.

        Args:
            utterances: A list of AnnotatedUtterance instances.
        """
        pass

    @abstractmethod
    def generate_utterance_text(
        self,
        intent: Intent,
        annotations: Optional[Union[List[Annotation], None]] = None,
        force_annotation: bool = False,
    ) -> Union[AnnotatedUtterance, bool]:
        """Textualizes a structured utterance using the templates.

        Args:
            intent: The underlying intent of the utterance.
            annotations: If provided, these annotations should be included in
              the utterance.
            force_annotation: A flag to indicate whether annotations should be
              forced or not.

        Returns:
            Generated response using templates.
        """
        pass

    @abstractmethod
    def dump_template(self, filepath: str) -> None:
        """Dump template to JSON format.

        Args:
            filepath: Destination path for the resulting JSON file."""
        pass

    @abstractmethod
    def _filter_templates(
        self,
        templates: List[AnnotatedUtterance],
        annotations: List[Annotation],
        force_annotation: bool,
    ) -> List[AnnotatedUtterance]:
        """Filters available templates based on annotations.

        Args:
            templates: Template annotated utterance.
            annotations: List of annotations to be used for filtering.
            force_annotation: If 'True' and annotations are provided templates
              without annotations will also be filtered out.

        Returns:
            List of annotated utterances that are possible to create with the
            provided annotations.
        """
        pass
