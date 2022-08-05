"""Interface defining core agent functionality.

This abstract class is to be subclassed both for bots and human ("Wizard of Oz")
agents.

An agent instance needs to be connected with a DialogueManager by invoking
`register_dialogue_manager()`.
"""
from __future__ import annotations

from enum import Enum

from dialoguekit.participant.participant import Participant

# TODO Some research needs to be done in how Python abstract classes work,
# to implement them for Agent and participant


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

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        return

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        return
