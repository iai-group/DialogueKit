"""Abstract interface for NLG."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue_act import DialogueAct


class AbstractNLG(ABC):
    """Represents a Natural Language Generation (NLG) component."""

    @abstractmethod
    def generate_utterance_text(
        self,
        dialogue_acts: List[DialogueAct],
        annotations: Optional[Union[List[Annotation], None]] = None,
        force_annotation: bool = False,
    ) -> Union[AnnotatedUtterance, bool]:
        """Turns a structured utterance into a textual one.

        This method is supposed to be implemented in a way that takes the
        arguments and returns a textual utterance, based on the arguments.

        Args:
            dialogue_acts: Dialogue acts of the utterance to be generated.
            annotations: If provided, these annotations should be considered
              during generation.
            force_annotation: A flag to indicate whether annotations should be
              forced or not.

        Returns:
            Generated response using templates.
            If generation fails, False should be returned.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError
