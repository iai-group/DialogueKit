from dialoguekit.core.utterance import Utterance


class NLU:
    """Represents a Natural Language Understanding (NLU) component."""

    def __init__(self) -> None:
        """Initializes the NLU component."""
        pass

    def get_intent(self, utterance: Utterance):
        """Classifies the intent of a given agent utterance."""
        # TODO: Add Intent class
        pass

    def get_slot_values(self, utterance: Utterance):
        """Extracts slot-value pairs from a given utterance."""
        pass
