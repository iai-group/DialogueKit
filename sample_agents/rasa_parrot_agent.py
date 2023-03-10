"""Simplest possible agent that parrots back everything the user says.

This agent depends on Rasa parrot project to parrot back. See
'docs/rasa-parrot.md' for more information
"""

import requests

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import DialogueParticipant


class RasaParrotAgent(Agent):
    def __init__(self, agent_id: str):
        """Rasa Parrot agent.

        This agent connects to the sample Rasa parrot agent found here:
        https://github.com/iai-group/dialoguekit/tree/main/external_agents

        To end the conversation the user has to say `EXIT`, `QUIT` or `STOP`.

        Args:
            agent_id: Agent id.
        """
        super().__init__(agent_id)
        self._RASA_URI = "http://localhost:5002/webhooks/rest/webhook"

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = AnnotatedUtterance(
            "Hello, I'm Rasa Parrot. What can I help u with?",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = AnnotatedUtterance(
            "It was nice talking to you. Bye",
            intent=self.stop_intent,
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        if utterance.text.lower() in ["quit", "stop", "exit"]:
            return

        r = requests.post(
            self._RASA_URI,
            json={
                "sender": "RasaParrotAgent",
                "message": "(Rasa Parroting) " + utterance.text,
            },
        )
        response = AnnotatedUtterance(
            r.json()[0]["text"],
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(response)
