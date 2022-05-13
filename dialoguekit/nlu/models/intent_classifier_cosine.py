"""Implements intent classification based on cosine similarity."""

from typing import List
import numpy as np
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlu.intent_classifier import IntentClassifier


class IntentClassifierCosine(IntentClassifier):
    def __init__(self, intents: List[Intent]) -> None:
        super().__init__(intents)
        self._labels = None
        self._tfidf_vectorizer = TfidfVectorizer()
        self._tfidf_matrix = None

    def train_model(
        self, utterances: List[Utterance], labels: List[Intent]
    ) -> None:
        """Trains a model based on a set of labeled utterances.

        Args:
            utterances: List of Utterance instances.
            labels: List of associated intent labels.
        """
        # Makes sure we have matching labels for all training utterances.
        assert len(utterances) == len(labels)
        self._labels = labels
        # Converts the training utterances into a TF-IDF-weighted term-document
        # matrix.
        self._tfidf_matrix = self._tfidf_vectorizer.fit_transform(
            [u.text for u in utterances]
        ).toarray()

    def get_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of an utterance based on based cosine
        similarity of TF-IDF-weighted term vectors.

        Args:
            utterance: An utterance.

        Returns:
            Predicted intent.
        """
        # Calculates the cosine similarities between the input utterance and
        # training utterances, based on TF-IDF vectors.
        sim_vector = cosine_similarity(
            self._tfidf_vectorizer.transform([utterance.text]).toarray(),
            self._tfidf_matrix,
        )[0]
        # Finds the most similar utterance based on cosine similarity, and
        # returns the corresponding intent as the prediction.
        max_idx = np.argmax(sim_vector)
        return self._labels[max_idx]

    def save_model(self, file_path: str) -> None:
        """Saves the trained model to a file.

        This method uses the joblib library to save the model.

        Args:
            file_path: File path.

        """
        dump(self._tfidf_matrix, f"{file_path}_matrix.joblib")
        dump(self._tfidf_vectorizer, f"{file_path}_vectorizer.joblib")
        dump(self._labels, f"{file_path}_labels.joblib")

    def load_model(self, file_path: str) -> None:
        """Loads a model from a file.

        This method uses the joblib library to load the model.

        Args:
            file_path: File path.

        """
        self._tfidf_matrix = load(f"{file_path}_matrix.joblib")
        self._tfidf_vectorizer = load(f"{file_path}_vectorizer.joblib")
        self._labels = load(f"{file_path}_labels.joblib")
