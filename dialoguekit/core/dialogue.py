"""Interface representing the sequence of utterances in a dialogue."""

from __future__ import annotations

import calendar
import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Text

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.feedback import UtteranceFeedback
from dialoguekit.participant import DialogueParticipant

if TYPE_CHECKING:
    from dialoguekit.core.utterance import Utterance


class Dialogue:
    def __init__(
        self, agent_id: str, user_id: str, conversation_id: str = None
    ) -> None:
        """Represents a dialogue.

        Args:
            agent_id: Agent ID.
            user_id: User ID.
            conversation_id: Conversation ID. Defaults to None.
        """
        self._agent_id = agent_id
        self._user_id = user_id
        if conversation_id is None:
            date = datetime.datetime.utcnow()
            utc_time = calendar.timegm(date.utctimetuple())
            self._conversation_id = (
                f"{self._agent_id}-{self._user_id}-{str(utc_time)}"
            )
        else:
            self._conversation_id = conversation_id
        self._utterances: List[Utterance] = []
        self._utterance_feedbacks: Dict[str, UtteranceFeedback] = {}
        self._metadata: Dict[str, Any] = {}

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
    def conversation_id(self) -> str:
        """Returns the conversation ID."""
        return self._conversation_id

    @property
    def agent_id(self) -> str:
        """Returns the agent ID."""
        return self._agent_id

    @property
    def user_id(self) -> str:
        """Returns the user ID."""
        return self._user_id

    @property
    def utterances(self) -> List[Utterance]:
        """Returns the utterances in the dialogue."""
        return self._utterances

    def get_utterance_feedback(self, utterance_id: str) -> UtteranceFeedback:
        """Returns feedback on given utterance."""
        return self._utterance_feedbacks[utterance_id]

    @property
    def metadata(self) -> Dict[str, Any]:
        """Returns the metadata of the dialogue."""
        return self._metadata

    @property
    def current_turn_id(self) -> int:
        """Returns the ID of the current utterance."""
        return len(self._utterances)

    def add_utterance(self, utterance: Utterance) -> None:
        """Adds an utterance to the history.

        Args:
            utterance: An instance of Utterance.
        """
        if utterance.utterance_id is None:
            utterance.utterance_id = "{}_{}_{}".format(
                self.conversation_id,
                (
                    self.agent_id
                    if utterance.participant is DialogueParticipant.AGENT
                    else self.user_id
                ),
                self.current_turn_id,
            )
        self._utterances.append(utterance)

    def add_utterance_feedback(
        self, utterance_feedback: UtteranceFeedback, utterance_id: str
    ) -> None:
        """Adds user's feedback on utterance level.

        The feedback previously added for a given utterance is overwritten.

        Args:
            utterance_feedback: User's feedback.
            utterance_id: Utterance ID.
        """
        self._utterance_feedbacks[utterance_id] = utterance_feedback

    def to_dict(self) -> Dict[str, Any]:
        """Converts the dialogue to a dictionary.

        Returns:
            Dialogue as dictionary.
        """
        dialogue_as_dict: Dict[str, Any] = {
            "conversation ID": self._conversation_id,
            "conversation": [],
            "agent": self._agent_id,
            "user": self._user_id,
        }
        if self._metadata:
            dialogue_as_dict["metadata"] = self._metadata

        for utterance in self.utterances:
            utterance_info: Dict[str, Any] = {
                "participant": utterance.participant.name,
                "utterance": utterance.text,
                "utterance ID": utterance.utterance_id,
            }

            feedback = self._utterance_feedbacks.get(utterance.utterance_id)
            if feedback is not None:
                utterance_info["utterance_feedback"] = feedback.feedback.value

            if isinstance(utterance, AnnotatedUtterance):
                dialogue_acts = list()
                for da in utterance.dialogue_acts:
                    dialogue_acts.append(
                        {
                            "intent": (
                                da.intent.label if da.intent is not None else ""
                            ),
                            "slot_values": [
                                [
                                    annotation.slot,
                                    annotation.value,
                                    annotation.start,
                                    annotation.end,
                                ]
                                for annotation in da.annotations
                            ],
                        }
                    )
                utterance_info["dialogue_acts"] = dialogue_acts

                for k, v in utterance.metadata.items():
                    utterance_info[k] = v

                annotations = utterance.annotations
                if annotations:
                    key_values = []
                    for annotation in annotations:
                        key_values.append([annotation.key, annotation.value])
                    utterance_info["annotations"] = key_values

            dialogue_as_dict["conversation"].append(utterance_info)
        return dialogue_as_dict
