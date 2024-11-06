"""Interface extending utterances with annotations."""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance


@dataclass(eq=True, unsafe_hash=True)
class AnnotatedUtterance(Utterance):
    """Represents an utterance, with annotations.

    The AnnotatedUtterance is a Utterance with additional information. In some
    cases we want to send an utterance with dialogue acts and/or Annotations.
    Dialogue acts are a specific type of annotation.
    """

    dialogue_acts: List[DialogueAct] = field(
        default_factory=list, compare=True, hash=False
    )
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

    def add_dialogue_acts(self, dialogue_acts: List[DialogueAct]) -> None:
        """Adds dialogue acts to the utterance.

        Args:
            dialogue_acts: List of dialogue acts.
        """
        self.dialogue_acts.extend(dialogue_acts)

    def get_intents(self) -> List[Intent]:
        """Returns utterance's intents."""
        return [da.intent for da in self.dialogue_acts]

    def num_dialogue_act_annotations(self) -> int:
        """Returns the number of slot-value annotations in dialogue acts."""
        return len(
            [
                annotation
                for da in self.dialogue_acts
                for annotation in da.annotations
            ]
        )

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
