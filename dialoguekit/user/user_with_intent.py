"""Abstract representation of core user-related data and functionality.

For communicating with an agent, the specific user instance needs to be
connected with a DialogueConnector by invoking
`register_dialogue_connector()`.
"""

from enum import Enum
from typing import Union

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.participant import DialogueParticipant, Participant


# TODO This needs to be updated to work with MathAgent
def find_operation_type(math_agent_utterance: str) -> Union[str, None]:
    """Find the correct operation type.

    Args:
        math_agent_utterance: Utterance to use.

    Returns:
        String with the operation type, or None if not found.
    """
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


class UserType(Enum):
    """Represents different types of users.

    This can be, humans vs simulated users.
    """

    HUMAN = 0
    SIMULATOR = 1


class UserWithIntent(Participant):
    def __init__(
        self,
        id: str,
        type: DialogueParticipant = DialogueParticipant.USER,
        user_type: UserType = UserType.HUMAN,
        intents=None,
    ) -> None:
        """Represents a user.

        Args:
            id: User ID.
            type: Agent type (default: USER).
            user_type: User type (default: HUMAN).
            intents: Intents that you want to select from.
        """
        super().__init__(id=id, type=type)
        self.user_type = user_type
        if intents is not None:
            self._intents = intents
        else:
            raise TypeError("You MUST define the possible intents for the User")

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called each time there is a new agent utterance.

        Args:
            utterance: Agent's utterance.
        """
        intent_menu = ""
        for i, intent in enumerate(self._intents):
            intent_menu += f"{i+1}: {intent.label}, "
        print(intent_menu)
        intent_selector = input("Select your desired intent: ")
        selected_intent = self._intents[int(intent_selector) - 1]

        text = input("Your response: ")
        response = AnnotatedUtterance(
            text, intent=selected_intent, participant=DialogueParticipant.USER
        )

        if selected_intent == Intent("ANSWER"):
            selected_intent = Intent(
                f"ANSWER.{find_operation_type(utterance.text)}"
            )
            response._intent = selected_intent
            response.add_annotation(Annotation(slot="NUMBER", value=text))

        self._dialogue_connector.register_user_utterance(response)
