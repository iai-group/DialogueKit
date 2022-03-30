"""Simplest possible agent that parrots back everything the user says.

This agent depends on Rasa parrot project to parrot back.
See docs/rasa-parrot.md for more information
"""

import requests
from dialoguekit.agent.agent import Agent
from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent


class RasaParrotAgent(Agent):
    """Rasa Parrot agent."""

    def __init__(self, agent_id: str):
        """Initializes agent.

        Args:
            agent_id: Agent id.
        """
        super().__init__(agent_id)
        self.__rasa_uri = "http://localhost:5002/webhooks/rest/webhook"

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = Utterance("Hello, I'm Rasa Parrot. What can I help u with?")
        self._dialogue_manager.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = Utterance(
            "It was nice talking to you. Bye", intent=Intent("EXIT")
        )
        self._dialogue_manager.register_agent_utterance(utterance)

    def receive_user_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        if utterance.text.lower() in ["quit", "stop", "exit"]:
            return

        r = requests.post(
            self.__rasa_uri,
            json={
                "sender": "RasaParrotAgent",
                "message": "(Rasa Parroting) " + utterance.text,
            },
        )
        response = Utterance(r.json()[0]["text"])
        self._dialogue_manager.register_agent_utterance(response)
