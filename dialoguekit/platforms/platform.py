"""The Platform facilitates displaying of the conversation."""

from dialoguekit.core.utterance import Utterance


class Platform:
    def __init__(self):
        """Represents a platform."""
        pass

    def display_agent_utterance(self, utterance: Utterance) -> None:
        """Diplays an agent utterance.

        Args:
            utterance: An instance of Utterance.
        """
        print(f"AGENT: {utterance.text}")

    def display_user_utterance(self, utterance: Utterance) -> None:
        """Diplays a user utterance.

        Args:
            utterance: An instance of Utterance.
        """
        print(f"USER:  {utterance.text}\n")
