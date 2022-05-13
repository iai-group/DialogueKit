"""Connector Agent to MovieBot.

This Agent is a connector to MovieBot. It relies on MovieBot to be running.
The messages are sent with POST requests and the response to the request is the
utterance from MovieBot.
"""

import requests
from dialoguekit.agent.agent import Agent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent


class MovieBotAgent(Agent):
    """Rasa Parrot agent."""

    def __init__(self, agent_id: str, uri: str = "http://127.0.0.1:5001"):
        """Initializes agent.

        Args:
            agent_id: Agent id.
        """
        super().__init__(agent_id)
        self._MOVIEBOT_URI = uri

    def welcome(self) -> None:
        """Sends the agent's welcome message."""

        r = requests.post(
            self._MOVIEBOT_URI,
            json={
                "entry": [
                    {
                        "messaging": [
                            {
                                "message": {"text": "/start"},
                                "sender": {"id": self.id},
                            }
                        ]
                    }
                ],
            },
        )
        response_raw = r.json()
        response = AnnotatedUtterance(
            response_raw["message"]["text"],
            intent=Intent(response_raw["message"]["intent"]),
        )
        self._dialogue_manager.register_agent_utterance(response)

    def goodbye(self) -> None:
        r = requests.post(
            self._MOVIEBOT_URI,
            json={
                "entry": [
                    {
                        "messaging": [
                            {
                                "message": {"text": "/exit"},
                                "sender": {"id": self.id},
                            }
                        ]
                    }
                ],
            },
        )
        response = AnnotatedUtterance(
            r.json()["message"]["text"], intent=Intent("EXIT")
        )
        self._dialogue_manager.register_agent_utterance(response)

    def receive_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """This method is called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        if annotated_utterance.text.lower() in ["quit", "stop", "exit"]:
            self.goodbye()

        r = requests.post(
            self._MOVIEBOT_URI,
            json={
                "entry": [
                    {
                        "messaging": [
                            {
                                "message": {"text": annotated_utterance.text},
                                "sender": {"id": self.id},
                            }
                        ]
                    }
                ],
            },
        )

        response_raw = r.json()
        print(response_raw["message"]["intent"])
        response = AnnotatedUtterance(
            response_raw["message"]["text"],
            intent=Intent(response_raw["message"]["intent"]),
        )
        self._dialogue_manager.register_agent_utterance(response)
