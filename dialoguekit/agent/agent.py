"""Interface defining core agent functionality.

This abstract class is to be subclassed both for bots and human ("Wizard of Oz")
agents.

An agent instance needs to be connected with a DialogueManager by invoking
`register_dialogue_manager()`.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

from dialoguekit.utterance.utterance import Utterance

if TYPE_CHECKING:
    from dialoguekit.manager.dialogue_manager import DialogueManager


class AgentType(Enum):
    """Represents different types of agents (bot vs. Wizard-of-Oz)."""

    BOT = 0
    WOZ = 1


class Agent(ABC):
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

    def register_dialogue_manager(
        self, dialogue_manager: DialogueManager
    ) -> None:
        """Registers the Dialogue Manager instance for the agent.

        Args:
            dialogue_manager: A DialogueManager instance.
        """
        self._dialogue_manager = dialogue_manager

    @abstractmethod
    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        pass

    @abstractmethod
    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        pass

    @abstractmethod
    def receive_user_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        pass
