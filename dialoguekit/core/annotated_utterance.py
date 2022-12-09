"""Interface extending utterances with annotations."""

import inspect
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.participant import DialogueParticipant


class AnnotatedUtterance(Utterance):
    def __init__(
        self,
        text: str,
        participant: DialogueParticipant,
        timestamp: Optional[datetime] = None,
        intent: Optional[Intent] = None,
        annotations: Optional[List[Annotation]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Represents an utterance, with additional annotations.

        The AnnotatedUtterance is a Utterance with additional information.
        In some cases we want to send an utterance with the Intent and or
        Annotations.

        Args:
            text: Utterance text.
            participant: The owner of the utterance.
            timestamp: When the utterance was uttered.
            intent: The intent of the utterance.
            annotations: Annotations of the Utterance text.
            metadata: Dict with optional attributes (satisfaction etc.).
        """
        super().__init__(
            text=text, participant=participant, timestamp=timestamp
        )
        self._intent = intent
        self._annotations = []
        if annotations:
            self._annotations.extend(annotations)
        self._metadata = metadata if metadata else {}

    def __str__(self) -> str:
        return self._text

    def __repr__(self) -> str:
        return f"AnnotatedUtterance({self._text})"

    def __hash__(self) -> int:
        hashed_annotations = "".join(
            [str(hash(annotation)) for annotation in self._annotations]
        )
        return hash((self._text, self._intent, hashed_annotations))

    def __eq__(self, __o: object) -> bool:
        """Comparison function."""
        if not isinstance(__o, AnnotatedUtterance):
            return False
        if self.utterance != __o.utterance:
            return False
        if self._intent != __o._intent:
            return False
        if len(self._annotations) != len(__o._annotations):
            return False
        if self._metadata != __o._metadata:
            return False

        for annotation in self._annotations:
            if annotation not in __o._annotations:
                return False

        return True

    @property
    def text(self) -> str:
        """Returns the utterance intent."""
        return self._text

    @property
    def intent(self) -> Intent:
        """Returns the utterance intent."""
        return self._intent

    @property
    def utterance(self) -> Utterance:
        """Returns the annotated utterance as a utterance."""
        return Utterance(
            text=self.text,
            participant=self._participant,
            timestamp=self._timestamp,
        )

    @property
    def participant(self) -> DialogueParticipant:
        """Returns the utterance participant."""
        return self._participant

    @property
    def metadata(self) -> Dict[str, Any]:
        """Returns the utterance metadata."""
        return self._metadata

    @classmethod
    def from_utterance(cls, utterance: Utterance):
        """Creates an instance of AnnotatedUtterance from an utterance."""
        properties = inspect.getmembers(
            utterance.__class__, predicate=lambda m: isinstance(m, property)
        )
        class_attributes = list(
            inspect.signature(AnnotatedUtterance).parameters
        )
        args = dict()
        for prop in properties:
            if prop[0] in class_attributes:
                getter = prop[1].fget
                args[prop[0]] = getter(utterance)
        return cls(**args)

    def add_annotation(
        self, annotation: Union[Annotation, List[Annotation]]
    ) -> None:
        """Adds an annotation to the utterance.

        Args:
            annotation: Annotation instance.
        """
        # TODO Only input List[Annotation] #130
        if isinstance(annotation, List):
            self._annotations.extend(annotation)
        elif isinstance(annotation, Annotation):
            self._annotations.append(annotation)
        else:
            raise TypeError(
                "Provided annotation is not of type Annotation or \
                    List[Annotation]"
            )

    def get_annotations(self) -> List[Annotation]:
        """Returns the available annotations for the utterance.

        Returns: List of Annotation instances.
        """
        return self._annotations

    def set_participant(self, participant: DialogueParticipant) -> None:
        """Sets the utterance participant type.

        Args:
            participant: Participant type who uttered the utterance.
        """
        self._participant = participant

    def get_text_placeholders(self) -> str:
        """Replaces the utterance text with placeholders.

        Returns:
            The utterance text with annotations replaced with placeholders.
        """
        # TODO See: https://github.com/iai-group/dialoguekit/issues/35
        return ""
