"""Abstract interface for dialogue policy.

The dialogue policy generates a dialogue act by the agent based on the current
dialogue state (last user's utterance and dialogue history). It defines the flow
of the conversation, i.e., what steps an agent must take at every stage. The
annotations of the dialogue act represent what the agent must elicit, recommend,
or inform. The output of the dialogue policy is converted to a natural language
response by the natural language generator.

For example, the dialogue act with intent ELICIT is generated if the agent does
not store any user preferences. For the user intent REVEAL, the dialogue policy
triggers the generation of an item recommendation (dialogue act with intent
RECOMMEND). 
"""

from abc import ABC, abstractmethod
from typing import List

from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.utterance import Utterance


class DialoguePolicy(ABC):
    def __init__(self) -> None:
        """Initializes the dialogue policy."""

    @abstractmethod
    def next_dialogue_act(
        user_utterance: Utterance, dialogue_history: List[Utterance]
    ) -> DialogueAct:
        """Returns the next dialogue act given the user utterance and history.

        This method is most likely used in receive_utterance() in the agent to
        generate the agent's response. Dialogue act prediction is composed of
        two steps: intent prediction and annotation prediction.

        Args:
            user_utterance: The last user utterance.
            dialogue_history: The dialogue history.

        Returns:
            The next dialogue act.
        """
        raise NotImplementedError
