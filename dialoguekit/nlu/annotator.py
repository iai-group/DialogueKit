"""Interface to annotate an utterance."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.utterance import Utterance


class Annotator(ABC):
    def __init__(self) -> None:
        """Initializes the annotator."""
        super().__init__()

    @abstractmethod
    def get_annotations(self, utterance: Utterance) -> List[Annotation]:
        """Annotates an utterance.

        Args:
            utterance: Utterance.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            List of annotations.
        """
        raise NotImplementedError

    @abstractmethod
    def save_annotator(self, path: str) -> None:
        """Saves the annotator to a given path.

        Args:
            path: Path to save the annotator.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load_annotator(self, path: str) -> Annotator:
        """Loads the annotator from a path.

        Args:
            path: Path to the annotator.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            Annotator.
        """
        raise NotImplementedError
