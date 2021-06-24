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
        """Initializes the intent classifier."""
        self.__utterance_intent_mapping = utterance_intent_mapping
        self.__docs = [
            text for text in list(self.__utterance_intent_mapping.keys())
        ]
        self.__tfidf_vectorizer = TfidfVectorizer()
        self.__tfidf_fit = self.__tfidf_vectorizer.fit(self.__docs)
        self.__tfidf_matrix = self.__tfidf_fit.transform(self.__docs).toarray()

    def get_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of a given agent utterance."""
        sim_vector = cosine_similarity(
            self.__tfidf_fit.transform([utterance.text]).toarray(),
            self.__tfidf_matrix.tolist(),
        )[0]
        sorted_sim_vector = sorted(
            range(len(sim_vector)), key=lambda i: sim_vector[i], reverse=True
        )[:1]
        return self.__utterance_intent_mapping.get(
            list(self.__utterance_intent_mapping.keys())[sorted_sim_vector[0]]
        )
