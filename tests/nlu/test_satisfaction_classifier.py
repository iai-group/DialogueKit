"""Tests for SatisfactionClassifier"""
import pytest
from dialoguekit.nlu.models.satisfaction_classifier import (
    SatisfactionClassifierSVM,
)


def test_initialization():
    SatisfactionClassifierSVM()


def test_tokenize_predict():
    sf = SatisfactionClassifierSVM()
    label = sf._tokenize_predict(
        input_text=["Whats the weather like? It raining as always."]
    )
    assert isinstance(label, list)
    assert label[0] == 2


def test_classify_text():
    sf = SatisfactionClassifierSVM()

    label_int = sf.classify_text(
        dialogue_text="Whats the weather like? It raining as always."
    )
    assert isinstance(label_int, int)
    assert label_int == 2

    label_list = sf.classify_text(
        dialogue_text=["Whats the weather like? It raining as always."]
    )
    assert isinstance(label_list, list)
    assert label_list[0] == 2


@pytest.mark.usefixtures("dialogue_history_1")
def test_classify_last_n_dialogue(dialogue_history_1):
    sf = SatisfactionClassifierSVM()

    label = sf.classify_last_n_dialogue(dialogue=dialogue_history_1, last_n=2)
    assert isinstance(label, int)
    assert label == 2

    label_full = sf.classify_last_n_dialogue(
        dialogue=dialogue_history_1, last_n=None
    )
    assert isinstance(label_full, int)
    assert label == 2
