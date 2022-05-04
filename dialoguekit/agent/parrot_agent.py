"""Simplest possible agent that parrots back everything the user says."""

from dialoguekit.agent.agent import Agent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent


class ParrotAgent(Agent):
    """Parrot agent."""

    def __init__(self, agent_id: str):
        """Initializes agent.

        Args:
            agent_id: Agent id.
        """
        super().__init__(agent_id)

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = AnnotatedUtterance(
            "Hello, I'm Parrot. What can I help u with?"
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = AnnotatedUtterance(
            "It was nice talking to you. Bye", intent=Intent("EXIT")
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def receive_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """This method is called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        response = AnnotatedUtterance("(Parroting) " + annotated_utterance.text)
        self._dialogue_manager.register_agent_utterance(response)
