"""Interface extending utterances with annotations."""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance


@dataclass(eq=True, unsafe_hash=True)
class AnnotatedUtterance(Utterance):
    """Represents an utterance, with additional annotations.

    The AnnotatedUtterance is a Utterance with additional information.
    In some cases we want to send an utterance with the Intent and or
    Annotations.
    """

    intent: Intent = field(default=None, hash=True)
    annotations: List[Annotation] = field(
        default_factory=list, compare=True, hash=False
    )
    metadata: Dict[str, Any] = field(
        default_factory=dict, compare=True, hash=False
    )

    def get_utterance(self) -> Utterance:
        """Returns the annotated utterance as a utterance."""
        return Utterance(
            text=self.text,
            utterance_id=self.utterance_id,
            participant=self.participant,
            timestamp=self.timestamp,
        )

    @classmethod
    def from_utterance(cls, utterance: Utterance):
        """Creates an instance of AnnotatedUtterance from an utterance."""
        args = asdict(utterance)
        return cls(**args)

    def add_annotations(self, annotations: List[Annotation]) -> None:
        """Adds annotations to the utterance.

        Args:
            annotations: List of annotations.
        """
        self.annotations.extend(annotations)

    def get_text_placeholders(self) -> str:
        """Replaces the utterance text with placeholders.

        Returns:
            The utterance text with annotations replaced with placeholders.
        """
        # TODO See: https://github.com/iai-group/dialoguekit/issues/35
        return ""
