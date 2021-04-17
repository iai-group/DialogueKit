"""Interface defining core agent functionality.

This abstract class is to be subclassed both for bots and human ("Wizard of Oz")
agents.

An agent instance needs to be connected with a DialogueManager by invoking
`register_dialogue_manager()`.
"""

from enum import Enum

# from dialoguekit.manager.dialogue_manager import DialogueManager
from dialoguekit.utterance.utterance import Utterance, UtteranceType


class AgentType(Enum):
    """Represents different types of agents (bot vs. Wizard-of-Oz)."""

    BOT = 0
    WOZ = 1


class Agent:
    """Represents an agent.

    TODO: Make abstract class and move current functionality to ParrotAgent.
    """

    def __init__(
        self, agent_id: str, agent_type: AgentType = AgentType.BOT
    ) -> None:
        """Initializes the agent.

        Args:
            agent_type: Agent type (default: BOT).
        """
        self.__agent_id = agent_id
        self._agent_type = agent_type
        self._dialogue_manager = None

    @property
    def agent_id(self):
        return self.__agent_id

    def connect_dialogue_manager(self, dialogue_manager) -> None:
        """Connects the Dialogue Manager instance for the agent.

        Args:
            dialogue_manager: A DialogueManager instance.

        TODO: Add type annotation for dialogue_manager.
        """
        self._dialogue_manager = dialogue_manager

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        # TODO: move particular implementation to ParrotAgent
        utterance = Utterance(
            "Hello, I'm Parrot. What can I help u with?", UtteranceType.WELCOME
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        # TODO: move particular implementation to ParrotAgent
        utterance = Utterance(
            "It was nice talking to you. Bye", UtteranceType.EXIT
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def receive_user_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        # TODO: move particular implementation to ParrotAgent
        response = Utterance("Parrot " + utterance.text)
        self._dialogue_manager.register_agent_utterance(response)
