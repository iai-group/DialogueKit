"""Simplest possible agent that parrots back everything the user says."""

from dialoguekit.agent.agent import Agent
from dialoguekit.utterance.utterance import Utterance, UtteranceType


class ParrotAgent(Agent):
    """Parrot agent."""

    def __init__(self):
        """Initializes agent."""
        super().__init__()

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = Utterance(
            "Hello, I'm Parrot. What can I help u with?", UtteranceType.WELCOME
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = Utterance(
            "It was nice talking to you. Bye", UtteranceType.EXIT
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def receive_user_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        response = Utterance("(Parroting) " + utterance.text)
        self._dialogue_manager.register_agent_utterance(response)
