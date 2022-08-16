"""Abstract interface for NLG."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent


class AbstractNLG(ABC):
    """Represents a Natural Language Generation (NLG) component."""

    @abstractmethod
    def generate_utterance_text(
        self,
        intent: Intent,
        annotations: Optional[Union[List[Annotation], None]] = None,
        force_annotation: bool = False,
    ) -> Union[AnnotatedUtterance, bool]:
        """Generates an annotated utterance.

        Args:
            intent: The underlying intent of the utterance.
            annotations: If provided, these annotations should be included in
              the utterance.
            force_annotation: A flag to indicate whether annotations should be
              forced or not.

        Returns:
            Generated response using templates.
            If generation fails, False should be returned.
        """
        pass
