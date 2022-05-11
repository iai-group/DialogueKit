"""User implementation that can specify reply Intent.

This User takes in a list of possible reply Intents, and then is asked to
specify the Intent of the reply. This is important to create a dialogue history
export for training user simulators as we then have the users Intent classified.

This implementation is tied to MathAgent, but can (and should) be abstracted for
use with other Agents.
"""

from typing import List, Union
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.participant.participant import Participant
from dialoguekit.core.intent import Intent
from dialoguekit.core.annotation import Annotation
from dialoguekit.user.user import UserType


# TODO This needs to be updated to work with MathAgent
def find_operation_type(math_agent_utterance: str):
    if "addition" in math_agent_utterance:
        return "ADDITION"
    elif "subtraction" in math_agent_utterance:
        return "SUBTRACTION"
    elif "multiplication" in math_agent_utterance:
        return "MULTIPLICATION"
    elif "division" in math_agent_utterance:
        return "DIVISION"
    else:
        return None


class MathUser(Participant):
    """Represents a user."""

    def __init__(
        self,
        id: str,
        type: UserType = UserType.HUMAN,
        intents: Union[List[Intent], None] = None,
    ) -> None:
        """Initializes the user.

        Args:
            user_id: User ID.
            user_type: User type (default: HUMAN).
        """
        super().__init__(id=id, type=type)
        if intents is not None:
            self._intents = intents
        else:
            raise TypeError("You MUST define the possible intents for the User")

    def receive_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """This method is called each time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        intent_menu = ""
        for i, intent in enumerate(self._intents):
            intent_menu += f"{i+1}: {intent.label}, "
        print(intent_menu)
        intent_selector = input("Select your desired intent: ")
        selected_intent = self._intents[int(intent_selector) - 1]

        text = input("Your response: ")
        response = AnnotatedUtterance(text, intent=selected_intent)

        if selected_intent == Intent("ANSWER"):
            selected_intent = Intent(
                f"ANSWER.{find_operation_type(annotated_utterance.text)}"
            )
            response._intent = selected_intent
            response.add_annotation(Annotation(slot="NUMBER", value=text))

        self._dialogue_manager.register_user_utterance(response)
