"""Interface representing a dialogue act.

For example in the following utterance, we have a dialogue act with an intent
and its annotations regarding the search for a restaurant:

>USER: I am looking for a cheap Turkish restaurant.
DialogueAct(
    intent = Intent("DISCLOSE"),
    annotations = [Annotation(food="Turkish"), Annotation(price_range="cheap")],
)

In the following utterance, the dialogue act only has an intent:
> USER: I like it.
DialogueAct(
    intent = Intent("DISCLOSE")
    annotations = []
)
"""

from dataclasses import dataclass, field
from typing import List

from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent


@dataclass(eq=True, unsafe_hash=True)
class DialogueAct:
    """Represents a dialogue act that is an intent and its annotations."""

    intent: Intent = field(default=None, hash=True)
    annotations: List[Annotation] = field(
        default_factory=list, compare=True, hash=False
    )
