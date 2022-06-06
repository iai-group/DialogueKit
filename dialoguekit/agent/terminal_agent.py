"""Terminal Agent.

An Agent that is used for testing with different Users.
Specifically if a User is actually a bot, it may be useful to test with the
Terminal Agent.
"""
from dialoguekit.participant.participant import Participant
from dialoguekit.core.intent import Intent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.agent.agent import AgentType


class TerminalAgent(Participant):
    """Represents an agent."""

    def __init__(self, id: str, type: AgentType = AgentType.BOT) -> None:
        """Initializes the agent.

        Args:
            id: Agent ID.
            type: Agent type (default: BOT).
        """
        super().__init__(id=id, type=type)

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        text = input("Your WELCOME message: ")
        response = AnnotatedUtterance(text)
        self._dialogue_manager.register_agent_utterance(response)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        text = input("Your GOODBYE message: ")
        response = AnnotatedUtterance(text, intent=Intent("EXIT"))
        response
        self._dialogue_manager.register_agent_utterance(response)

    def receive_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        text = input("Your response: ")
        response = AnnotatedUtterance(text)
        self._dialogue_manager.register_agent_utterance(response)
