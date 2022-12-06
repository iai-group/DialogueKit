"""Simple mathematics agent, that asks math questions."""

# TODO Remove MathAgent
# See: https://github.com/iai-group/DialogueKit/issues/162

import math
import random
from enum import Enum
from typing import Optional

from dialoguekit.agent.agent import Agent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.annotation import Annotation
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlg.nlg_template import TemplateNLG
from dialoguekit.nlg.template_from_training_data import (
    build_template_from_instances,
)
from dialoguekit.participant.participant import DialogueParticipant


class Operation(Enum):
    ADDITION = 0
    SUBTRACTION = 1
    MULTIPLICATION = 2
    DIVISION = 3


class MathAgent(Agent):
    def __init__(
        self,
        agent_id: str,
        nlg: Optional[TemplateNLG] = None,
    ) -> None:
        """Mathematics agent.

        This Agent will ask for help with some simple math questions. These
        questions are of the form "What is 5 + 1?". If the User responds with
        the right answer it will ask a new question. If the User responds with
        the wrong answer the MathAgent will respond that the provided answer was
        not correct.

        Args:
            agent_id: Agent id.
            nlg: If set, it will override the internal NLG.
        """
        super().__init__(agent_id)
        self._nlg = nlg
        self._expected_answer: float
        self._initialize_nlu_nlg()

    def _initialize_nlu_nlg(self) -> None:
        """Initializes the NLG module.

        If no NLG template was provided during initialization, this
        method will create a basic NLG template.
        """
        if self._nlg is None:

            a1 = AnnotatedUtterance(
                intent=Intent("OPERATION.ADDITION"),
                text="What is 5 + 6 ?",
                annotations=[
                    Annotation(slot="NUMBER", value="6"),
                    Annotation(slot="NUMBER", value="5"),
                ],
                participant=DialogueParticipant.AGENT,
            )
            a2 = AnnotatedUtterance(
                intent=Intent("OPERATION.SUBTRACTION"),
                text="What is 5 subtraction 6 ?",
                annotations=[
                    Annotation(slot="NUMBER", value="6"),
                    Annotation(slot="NUMBER", value="5"),
                ],
                participant=DialogueParticipant.AGENT,
            )
            a3 = AnnotatedUtterance(
                intent=Intent("OPERATION.MULTIPLICATION"),
                text="What is 5 multiplication 6 ?",
                annotations=[
                    Annotation(slot="NUMBER", value="6"),
                    Annotation(slot="NUMBER", value="5"),
                ],
                participant=DialogueParticipant.AGENT,
            )
            a4 = AnnotatedUtterance(
                intent=Intent("OPERATION.DIVISION"),
                text="What is 5 division 6 ?",
                annotations=[
                    Annotation(slot="NUMBER", value="6"),
                    Annotation(slot="NUMBER", value="5"),
                ],
                participant=DialogueParticipant.AGENT,
            )

            a5 = AnnotatedUtterance(
                intent=Intent("WRONG"),
                text="Thats not quite right! \nTry again.",
                participant=DialogueParticipant.AGENT,
            )
            a6 = AnnotatedUtterance(
                intent=Intent("WRONG"),
                text="Thats wrong. \nTry again.",
                participant=DialogueParticipant.AGENT,
            )
            utterances = [a1, a2, a3, a4, a5, a6, a6]

            responses_template = build_template_from_instances(
                utterances=utterances
            )
            self._nlg = TemplateNLG(responses_template)

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = AnnotatedUtterance(
            """Hello, I'm a bot in need of some help.
            Can you help me with some mathematics?""",
            intent=Intent("WELCOME"),
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = AnnotatedUtterance(
            "It was nice talking to you. Bye",
            intent=Intent("EXIT"),
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        answered = False
        try:
            response_answer = float(utterance.text)
            if not math.isclose(float(response_answer), self._expected_answer):
                answered = True
                response = self._nlg.generate_utterance_text(
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
            if operation == Operation.ADDITION:
                self._expected_answer = number_1 + number_2
            elif operation == Operation.SUBTRACTION:
                self._expected_answer = number_1 - number_2
            elif operation == Operation.MULTIPLICATION:
                self._expected_answer = number_1 * number_2
            elif operation == Operation.DIVISION:
                self._expected_answer = number_1 / number_2

            # TODO Add better comparison
            self._expected_answer = math.floor(self._expected_answer * 10) / 10

            response = self._nlg.generate_utterance_text(
                intent=Intent(str(operation)),
                annotations=[
                    Annotation(slot="NUMBER", value=str(number_1)),
                    Annotation(slot="NUMBER", value=str(number_2)),
                ],
            )
            response.set_participant(DialogueParticipant.AGENT)

        self._dialogue_manager.register_agent_utterance(response)
