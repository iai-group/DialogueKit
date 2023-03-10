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

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent, AgentType
from dialoguekit.participant.participant import DialogueParticipant

_MOVIEBOT_DEFAULT_URI = "http://127.0.0.1:5001"
_MOVIEBOT_STOP_INTENT = Intent("END")


class MovieBotAgent(Agent):
    def __init__(
        self,
        agent_id: str,
        uri: str = _MOVIEBOT_DEFAULT_URI,
        stop_intent: Intent = _MOVIEBOT_STOP_INTENT,
    ) -> None:
        """Moviebot connector agent.

        Uses POST requests to MovieBot server as communication platform.

        Args:
            agent_id: Agent id.
            uri: MovieBot server address.
            stop_intent: MovieBot stop intent.
        """
        super().__init__(
            agent_id, agent_type=AgentType.BOT, stop_intent=stop_intent
        )
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
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(response)

    def goodbye(self) -> None:
        """Sends exit request to MovieBot."""
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
            r.json()["message"]["text"],
            intent=self.stop_intent,
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(response)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called each time there is a new user utterance.

        Args:
            utterance: User utterance.
        """
        if utterance.text.lower() in ["quit", "stop", "exit"]:
            self.goodbye()

        r = requests.post(
            self._MOVIEBOT_URI,
            json={
                "entry": [
                    {
                        "messaging": [
                            {
                                "message": {"text": utterance.text},
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
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(response)
