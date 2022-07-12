"""Connector Agent to IAI MovieBot.

This Agent is a connector to MovieBot. It relies on MovieBot to be running.
The messages are sent with POST requests and the response to the request is the
utterance from MovieBot.

The IAI MovieBot can be downloaded from here:
https://github.com/iai-group/moviebot

As the current release of the bot does not support our usecase you need to
checkout the 'separate-flask-server' branch. Follow the IAI MovieBot
installation instructions. The provided config in this branch will start the
server with the right configuration.
"""

import requests
from dialoguekit.agent.agent import Agent, AgentType
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent


_MOVIEBOT_DEFAULT_URI = "http://127.0.0.1:5001"


class MovieBotAgent(Agent):
    """MovieBot connector agent.

    Uses POST requests to MovieBot server as communication platform.
    """

    def __init__(self, agent_id: str, uri: str = _MOVIEBOT_DEFAULT_URI) -> None:
        """Initializes agent.

        Args:
            agent_id: Agent id.
            uri: MovieBot server address.
        """
        super().__init__(agent_id, type=AgentType.BOT)
        self._MOVIEBOT_URI = _MOVIEBOT_DEFAULT_URI

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
        """Sends exit request to MovieBot"""
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
            annotated_utterance: User annotated utterance.
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
