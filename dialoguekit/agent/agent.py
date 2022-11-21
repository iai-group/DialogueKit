"""Interface defining core agent functionality.

This abstract class is to be subclassed both for bots and human ("Wizard of Oz")
agents.

An agent instance needs to be connected with a DialogueConnector by invoking
`register_dialogue_connector()`.
"""
from __future__ import annotations

from enum import Enum

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.participant.participant import DialogueParticipant, Participant

# TODO Some research needs to be done in how Python abstract classes work,
# to implement them for Agent and participant


class AgentType(Enum):
    """Represents different types of agents (bot vs Wizard-of-Oz)."""

    BOT = 0
    WOZ = 1


class Agent(Participant):
    def __init__(self, id: str, agent_type: AgentType = AgentType.BOT) -> None:
        """Represents an agent.

        Args:
            id: Agent ID.
            agent_type: Agent type (default: BOT).
        """
        super().__init__(id=id, type=DialogueParticipant.AGENT)
        self._agent_type = agent_type

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        return

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        return

    def receive_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Gets called each time there is a new user utterance.

        Args:
            annotated_utterance: User utterance.
        """
