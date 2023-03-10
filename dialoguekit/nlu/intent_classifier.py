"""Abstract interface for intent classification.

This interface assumes a single intent per utterance, i.e., approaches
the task as a single-label classification problem. The generalization to
multi-label classification is left to future work.
"""

from abc import ABC, abstractmethod
from typing import Dict, List

from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance


class IntentClassifier(ABC):
    def __init__(self, intents: List[Intent]) -> None:
        """Initializes the intent classifier.

        Args:
            intents: List of allowed intents.
        """
        self._intents: Dict[str, Intent] = {i.label: i for i in intents}

    @abstractmethod
    def train_model(
        self, utterances: List[Utterance], labels: List[Intent]
    ) -> None:
        """Trains a model based on a set of labeled utterances.

        Args:
            utterances: List of Utterance instances.
            labels: List of associated intent labels.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError

    @abstractmethod
    def classify_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of an utterance.

        Args:
            utterance: An utterance.

        Returns:
            Predicted intent.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError

    @abstractmethod
    def save_model(self, file_path: str) -> None:
        """Saves the trained model to a file.

        Args:
            file_path: File path.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError

    @abstractmethod
    def load_model(self, file_path: str) -> None:
        """Loads a model from a file.

        Args:
            file_path: File path.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError
