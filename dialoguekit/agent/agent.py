"""Interface defining core agent functionality.

This abstract class is to be subclassed both for bots and human ("Wizard of Oz")
agents.

An agent instance needs to be connected with a DialogueManager by invoking
`register_dialogue_manager()`.
"""

from __future__ import annotations
from enum import Enum

from dialoguekit.utterance.utterance import Utterance, UtteranceType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dialoguekit.manager.dialogue_manager import DialogueManager


class AgentType(Enum):
    """Represents different types of agents (bot vs. Wizard-of-Oz)."""

    BOT = 0
    WOZ = 1


class Agent:
    """Represents an agent.

    TODO: Make abstract class and move current functionality to ParrotAgent.
    """

    def __init__(self, agent_type: AgentType = AgentType.BOT) -> None:
        """Initializes the agent.

        Args:
            agent_type: Agent type (default: BOT).
        """
        self._agent_type = agent_type
        self._dialogue_manager = None

    def register_dialogue_manager(self, dialogue_manager: DialogueManager) -> None:
        """Registers the Dialogue Manager instance for the agent.

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
