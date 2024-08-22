"""Simplest possible agent that parrots back everything the user says."""

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import DialogueParticipant


class ParrotAgent(Agent):
    def __init__(self, id: str):
        """Parrot agent.

        This agent parrots back what the user utters.
        To end the conversation the user has to say `EXIT`.

        Args:
            id: Agent id.
        """
        super().__init__(id)

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = AnnotatedUtterance(
            "Hello, I'm Parrot. What can I help u with?",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = AnnotatedUtterance(
            "It was nice talking to you. Bye",
            dialogue_acts=[DialogueAct(intent=self.stop_intent)],
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called each time there is a new user utterance.

        If the received message is "EXIT" it will close the conversation.

        Args:
            utterance: User utterance.
        """
        if utterance.text == "EXIT":
            self.goodbye()
            return

        response = AnnotatedUtterance(
            "(Parroting) " + utterance.text,
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(response)
