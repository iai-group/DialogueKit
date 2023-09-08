"""A module for tracking the state of a dialogue."""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.participant.participant import DialogueParticipant


@dataclass
class DialogueState:
    """A class to represent the state of a dialogue"""

    history: List[AnnotatedUtterance] = field(default_factory=list)
    last_user_intent: str = None
    slots: Dict[str, List[Annotation]] = field(
        default_factory=lambda: defaultdict(list)
    )
    turn_count: int = 0


class DialogueStateTracker:
    def __init__(self) -> None:
        """Initializes the dialogue state tracker"""
        self._dialogue_state = DialogueState()

    def get_state(self) -> DialogueState:
        """Returns the current state of the dialogue.

        Returns:
            The current state of the dialogue.
        """
        return self._dialogue_state

    def update(self, annotated_utterance: AnnotatedUtterance) -> None:
        """Updates the dialogue state with the annotated utterance.

        Args:
            annotated_utterance: The annotated utterance.
        """
        self._dialogue_state.history.append(annotated_utterance)
        if annotated_utterance.participant is not DialogueParticipant.USER:
            return

        self._dialogue_state.last_user_intent = annotated_utterance.intent

        for annotation in annotated_utterance.annotations:
            self._dialogue_state.slots[annotation.slot].append(annotation)

        self._dialogue_state.turn_count += 1
