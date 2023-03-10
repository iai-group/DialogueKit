"""Interface defining core agent functionality.

This abstract class is to be subclassed both for bots and human ("Wizard of Oz")
agents.

An agent instance needs to be connected with a DialogueConnector by invoking
`register_dialogue_connector()`.
"""
from __future__ import annotations

from abc import abstractmethod
from enum import Enum

from dialoguekit.core.intent import Intent
from dialoguekit.participant.participant import DialogueParticipant, Participant


class AgentType(Enum):
    """Represents different types of agents (bot vs Wizard-of-Oz)."""

    BOT = 0
    WOZ = 1


class Agent(Participant):
    def __init__(
        self,
        id: str,
        agent_type: AgentType = AgentType.BOT,
        stop_intent: Intent = Intent("EXIT"),
    ) -> None:
        """Represents an agent.

        Args:
            id: Agent ID.
            agent_type: Agent type (default: BOT).
            stop_intent: Label of the exit intent. Defaults to "EXIT".
        """
        super().__init__(id=id, type=DialogueParticipant.AGENT)
        self._agent_type = agent_type
        self._stop_intent = stop_intent

    @property
    def stop_intent(self) -> Intent:
        """Returns the agent's stop intent."""
        return self._stop_intent

    @abstractmethod
    def welcome(self) -> None:
        """Sends the agent's welcome message.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError

    @abstractmethod
    def goodbye(self) -> None:
        """Sends the agent's goodbye message.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError
