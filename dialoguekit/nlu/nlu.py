from dialoguekit.utterance.utterance import Utterance


class NLU:
    """Represents a Natural Language Understanding (NLU) component."""

    def __init__(self) -> None:
        """Initializes the NLU component."""
        pass

    def get_intent(self, utterance: Utterance):
        """Classifies the intent of a given agent utterance."""
        # TODO: Add Intent class
        pass

    def get_entities(self, utterance: Utterance):
        """Detects entities a given agent utterance."""
        # TODO: Add Entity class
        pass
