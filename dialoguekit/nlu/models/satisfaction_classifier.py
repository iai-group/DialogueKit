"""Satisfaction classification.

The SVM model and data it was trained on are based on:
https://github.com/sunnweiwei/user-satisfaction-simulation
"""

from joblib import load
from typing import Union, List, Optional
from dialoguekit.core.dialogue import Dialogue

from pathlib import Path


SATISFACTION_CLASSIFIER_MODEL_PATH = "LinearSVC_2_0.joblib"
SATISFACTION_TOKENIZER_PATH = "vectorizer_2_0.joblib"


class SatisfactionClassifier:
    def __init__(self) -> None:
        path_to_models = Path(__file__).parent / "satisfaction"
        tokenizer_path = path_to_models.joinpath(SATISFACTION_TOKENIZER_PATH)
        classifier_path = path_to_models.joinpath(
            SATISFACTION_CLASSIFIER_MODEL_PATH
        )
        self._model_svm = load(str(classifier_path))
        self._tokenizer = load(str(tokenizer_path))

    def _tokenize_predict(self, input_text: List[str]) -> List[int]:
        """Tokenize and classify satisfaction.

        Note: Every separate string will be predicted by its own. Thus if you
        want to predict upon a back-and-forth dialogue, it has to be reflected
        in each string by it self.

        Args:
            input_text: list of text to classified

        Returns:
            List of classifications for every string in the input.
        """
        transformed_strings = self._tokenizer.transform(input_text)
        satisfaction = self._model_svm.predict(transformed_strings)
        return list(satisfaction)

    def classify_text(
        self, dialogue_text: Union[str, List[str]]
    ) -> Union[int, List[int]]:
        """Classify text.

        Allows for both list of string and a single string.

        Args:
            dialogue_text: Text to be classified.

        Returns:
            If the provided input is a list, a list will be returned.
            If the input is a string, the return will be a single int.
        """

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
        """Classify the n last in the dialogue.

        If 'last_n' is None the whole dialogue will be classified.

        Args:
            dialogue: Dialogue to classify
            last_n: How many of the last utterances in the dialogue to use for
                    the classification.

        Raises:
            TypeError: If 'last_n' is greater then the length of the dialogue.

        Returns:
            Satisfaction classification.
        """

        if last_n is None:
            last_n = len(dialogue.utterances)

        complete_dialogue_text = " .".join(
            [
                annotated_utterance["utterance"].text
                for annotated_utterance in dialogue.utterances[-last_n:]
            ]
        )
        return int(self._tokenize_predict([complete_dialogue_text])[0])
