"""Abstract representation of core user-related data and functionality.

For communicating with an agent, the specific user instance needs to be
connected with a DialogueManager by invoking `register_dialogue_manager()`.
"""

from __future__ import annotations
from enum import Enum

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.participant.participant import Participant
from dialoguekit.core.intent import Intent


def find_operation_type(math_agent_utterance: str):
    if "+" in math_agent_utterance:
        return "ADDITION"
    elif "-" in math_agent_utterance:
        return "SUBTRACTION"
    elif "*" in math_agent_utterance:
        return "MULTIPLICATION"
    elif "/" in math_agent_utterance:
        return "DIVISION"
    else:
        return None


class UserType(Enum):
    """Represents different types of users (humans vs. simulated users)."""

    HUMAN = 0
    SIMULATOR = 1


class UserWithIntent(Participant):
    """Represents a user."""

    def __init__(
        self, id: str, type: UserType = UserType.HUMAN, intents=None
    ) -> None:
        """Initializes the user.

        Args:
            user_id: User ID.
            user_type: User type (default: HUMAN).
        """
        super().__init__(id=id, type=type)
        if intents is not None:
            self.__intents = intents
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
        for i, intent in enumerate(self.__intents):
            intent_menu += f"{i+1}: {intent.label}, "
        print(intent_menu)
        intent_selector = input("Select your desiered intent: ")
        selected_intent = self.__intents[int(intent_selector) - 1]
        if find_operation_type(
            annotated_utterance.text
        ) is not None and selected_intent == Intent("ANSWER"):
            selected_intent = Intent(
                f"ANSWER.{find_operation_type(annotated_utterance.text)}"
            )

        text = input("Your response: ")
        response = AnnotatedUtterance(text, intent=selected_intent)
        self._dialogue_manager.register_user_utterance(response)
