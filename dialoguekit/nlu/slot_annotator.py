"""Interface for slot annotation."""

import abc
from typing import List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.utterance import Utterance


class SlotAnnotator(abc.ABC):
    def __init__(self) -> None:
        """Instantiates a slot annotator."""
        super().__init__()

    @abc.abstractmethod
    def get_annotations(self, utterance: Utterance) -> List[Annotation]:
        """Annotates utterance.

        Args:
            utterance: Utterance to annotate.

        Raises:
            NotImplementedError: If not implemented in derived class.

        Returns:
            List of annotations.
        """
        raise NotImplementedError
