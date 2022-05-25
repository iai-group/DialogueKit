"""Satisfaction classification"""

from joblib import load
from typing import Union, List, Optional
from dialoguekit.core.dialogue import Dialogue


SATISFACTION_CLASSIFIER_MODEL_PATH = (
    "dialoguekit/nlu/models/satisfaction/LinearSVC_2_0.joblib"
)
SATISFACTION_TOKENIZER_PATH = "dialoguekit/nlg/models/vectorizer_2_0.joblib"


class SatisfactionClassifier:
    def __init__(self) -> None:
        self._model_svm = load(SATISFACTION_CLASSIFIER_MODEL_PATH)
        self._tokenizer = load(SATISFACTION_TOKENIZER_PATH)

    def _tokenize_predict(self, input_text: List[str]) -> List[int]:
        transformed_strings = self._tokenizer.transform(input_text)
        satisfaction = self._model_svm.predict(transformed_strings)
        return list(satisfaction)

    def classify_text(
        self, dialogue_text: Union[str, List[str]]
    ) -> Union[int, List[int]]:

        input_type = type(dialogue_text)
        if isinstance(dialogue_text, str):
            dialogue_text = [dialogue_text]

        satisfaction = self._tokenize_predict(dialogue_text)

        if input_type == str:
            return int(satisfaction[0])
        return list(satisfaction)

    def classify_last_n_dialogue(
        self, dialogue: Dialogue, last_n: Optional[Union[int, None]] = None
    ) -> int:

        if last_n is None:
            last_n = len(dialogue.utterances)
        elif last_n > len(dialogue.utterances):
            raise TypeError(
                f"last_n: {last_n} is longer then the length of the dialogue: \
                    {len(dialogue.utterances)}."
            )

        complete_dialogue_text = " .".join(
            [
                annotated_utterance["utterance"].text
                for annotated_utterance in dialogue.utterances[:-last_n]
            ]
        )
        return int(self._tokenize_predict([complete_dialogue_text])[0])
