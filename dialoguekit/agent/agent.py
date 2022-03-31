"""Interface defining core agent functionality.

This abstract class is to be subclassed both for bots and human ("Wizard of Oz")
agents.

An agent instance needs to be connected with a DialogueManager by invoking
`register_dialogue_manager()`.
"""
from __future__ import annotations
from dialoguekit.participant.participant import Participant
from abc import abstractmethod
from enum import Enum


class AgentType(Enum):
    """Represents different types of agents (bot vs. Wizard-of-Oz)."""

    BOT = 0
    WOZ = 1


class Agent(Participant):
    """Represents an agent."""

    def __init__(self, id: str, type: AgentType = AgentType.BOT) -> None:
        """Initializes the agent.

        Args:
            id: Agent ID.
            type: Agent type (default: BOT).
        """
        super().__init__(id=id, type=type)

    @abstractmethod
    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        pass

    @abstractmethod
    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        pass
