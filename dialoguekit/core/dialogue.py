"""Interface representing the sequence of utterances in a dialogue."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Text

from dialoguekit.core.utterance import Utterance


class DialogueParticipant(Enum):
    """Represents possible dialogue participants."""

    AGENT = 0
    USER = 1


class Dialogue:
    """Represents a dialogue."""

    def __init__(self, agent_id: str, user_id: str) -> None:
        """Initializes the dialogue history.

        Args:
            agent_id: Agent ID.
            user_id: User ID.
        """
        self._agent_id = agent_id
        self._user_id = user_id
        self._utterances = []
        self._metadata = {}

    def __str__(self) -> Text:
        return f"Dialogue(agent_id={self._agent_id}, user_id={self._user_id})"

    def __repr__(self) -> Text:
        return f"Dialogue(agent_id={self._agent_id}, user_id={self._user_id})"

    def __eq__(self, _o: object) -> bool:
        if not isinstance(_o, Dialogue):
            return False
        if self._agent_id != _o._agent_id:
            return False
        if self._user_id != _o._user_id:
            return False
        if len(self._utterances) != len(_o._utterances):
            return False
        for annotation in self._utterances:
            if annotation not in _o._utterances:
                return False

        return True

    @property
    def agent_id(self) -> str:
        return self._agent_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def utterances(self) -> List[Dict]:
        return self._utterances

    def _add_utterance(
        self, sender: DialogueParticipant, utterance: Utterance
    ) -> None:
        """Adds an utterance to the history.

        Args:
            sender: Sender of the utterance (AGENT or USER).
            utterance: An instance of Utterance.
        """
        self._utterances.append(
            {
                "sender": sender,
                "timestamp": datetime.now(),
                "utterance": utterance,
            }
        )

    def add_agent_utterance(self, utterance: Utterance) -> None:
        """Adds an agent utterance.

        Args:
            utterance: An instance of utterance.
        """
        self._add_utterance(DialogueParticipant.AGENT, utterance)

    def add_user_utterance(self, utterance: Utterance) -> None:
        """Adds a user utterance.

        Args:
            utterance: An instance of utterance.
        """
        self._add_utterance(DialogueParticipant.USER, utterance)
