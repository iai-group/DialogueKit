"""Simplest possible agent that parrots back everything the user says."""

import random
from typing import Optional
from enum import Enum
import math

from dialoguekit.agent.agent import Agent
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent
from dialoguekit.nlg.nlg import NLG
from dialoguekit.nlu.nlu import NLU


class Operation(Enum):
    plus = 0
    minus = 1
    multiplication = 2
    division = 3


class MathAgent(Agent):
    """Parrot agent."""

    def __init__(
        self,
        agent_id: str,
        nlu: Optional[NLU] = None,
        nlg: Optional[NLG] = None,
    ):
        """Initializes agent.

        Args:
            agent_id: Agent id.
            nlu: if set it will overide the internal nlu
            nlg: if set it will overide the internal nlg
        """
        super().__init__(agent_id)
        self.__nlu = nlu
        self.__nlg = nlg
        self.__initialize_nlu_nlg()

    def __initialize_nlu_nlg(self):

        if self.__nlu is None:
            # intents = [Intent("QUESTION"), Intent("ANSWER")]
            pass
        if self.__nlg is None:
            a1 = AnnotatedUtterance(
                intent=Intent("QUESTION"), text="What is 5 + 6 ?"
            )
            a1.add_annotation(annotation=Annotation(slot="NUMBER", value="6"))
            a1.add_annotation(annotation=Annotation(slot="NUMBER", value="5"))
            a1.add_annotation(
                annotation=Annotation(slot="OPERATION", value="+")
            )
            a2 = AnnotatedUtterance(
                intent=Intent("WRONG"),
                text="Thats not quite right! \nTry again.",
            )
            a3 = AnnotatedUtterance(
                intent=Intent("WRONG"), text="Thats wrong. \nTry again."
            )
            utterances = [a1, a2, a3]

            self.__nlg = NLG()
            self.__nlg.template_from_objects(utterances=utterances)

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = AnnotatedUtterance(
            """Hello, I'm a bot in need of some help.
            Can you help me with some mathematics?"""
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = AnnotatedUtterance(
            "It was nice talking to you. Bye", intent=Intent("EXIT")
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def receive_user_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new user utterance.


        Args:
            utterance: User utterance.
        """
        answered = False
        try:
            response_answer = float(utterance.text)
            if response_answer != self.__expected_answer:
                answered = True
                response = self.__nlg.generate_utterance_text(
                    intent=Intent("WRONG"), annotations=[]
                )

        except ValueError:
            pass

        if utterance.text == "EXIT":
            self.goodbye()
            return

        elif not answered:  # Later check if right INTENT
            number_1 = random.randint(1, 10)
            number_2 = random.randint(1, 10)
            operation = random.choice(list(Operation))
            if operation.value == 0:
                self.__expected_answer = number_1 + number_2
                operation_symbol = "+"
            elif operation.value == 1:
                self.__expected_answer = number_1 - number_2
                operation_symbol = "-"
            elif operation.value == 2:
                self.__expected_answer = number_1 * number_2
                operation_symbol = "*"
            elif operation.value == 3:
                self.__expected_answer = number_1 / number_2
                operation_symbol = "/"

            # TODO Add better comparison
            self.__expected_answer = (
                math.floor(self.__expected_answer * 10) / 10
            )

            response = self.__nlg.generate_utterance_text(
                intent=Intent("QUESTION"),
                annotations=[
                    Annotation(slot="NUMBER", value=str(number_1)),
                    Annotation(slot="OPERATION", value=operation_symbol),
                    Annotation(slot="NUMBER", value=str(number_2)),
                ],
            )

        self._dialogue_manager.register_agent_utterance(response)


if __name__ == "__main__":
    agent = MathAgent(agent_id="test")
