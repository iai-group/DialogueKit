#!/usr/bin/env python3
"""Implements intent classification based on cosine similarity."""
from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance


class IntentClassifierCosine:
    """Cosine similarity based intent classifier."""

    def __init__(self, utterance_intent_mapping: Dict) -> None:
        """Initializes the intent classifier.

        Args:
            utterance_intent_mapping: utterence intent dict {utterence: intent}
        """
        self.__utterance_intent_mapping = utterance_intent_mapping
        # List of agent utterances
        self.__utterances = [
            text for text in list(self.__utterance_intent_mapping.keys())
        ]
        # Instantiates the vectorizer object
        self.__tfidf_vectorizer = TfidfVectorizer()
        # Converts the agent utterances into a VSM matrix,
        # where tf-idf (idf optionally) of any term can be fetched based on this matrix
        self.__tfidf_fit = self.__tfidf_vectorizer.fit(self.__utterances)
        self.__tfidf_matrix = self.__tfidf_fit.transform(self.__utterances).toarray()

    def get_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of a given agent utterance.

        Args:
            utterance: agent utterance.

        Returns:
            Intent of agent utterance based on tf-based cosine similarity.
        """
        # Calculates the cosine similarities between the input agent and backend utterances
        # based on tf-idf vectors (idf is configurable).
        sim_vector = cosine_similarity(
            self.__tfidf_fit.transform([utterance.text]).toarray(),
            self.__tfidf_matrix,
        )[0]
        # Finds the most similar utterance based on cosine similarities
        sorted_sim_vector = sorted(
            range(len(sim_vector)), key=lambda i: sim_vector[i], reverse=True
        )[:1]
        return self.__utterance_intent_mapping.get(
            list(self.__utterance_intent_mapping.keys())[sorted_sim_vector[0]]
        )
