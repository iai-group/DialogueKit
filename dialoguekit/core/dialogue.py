"""Interface representing the sequence of utterances in a dialogue."""

from typing import List, Text

from dialoguekit.core.utterance import Utterance


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
        self._utterances: Utterance = []
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
    def utterances(self) -> List[Utterance]:
        return self._utterances

    def add_utterance(self, utterance: Utterance) -> None:
        """Adds an utterance to the history.

        Args:
            utterance: An instance of Utterance.
        """
        self._utterances.append(utterance)
