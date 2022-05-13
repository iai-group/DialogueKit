"""Simplest possible agent that parrots back everything the user says.

This agent depends on Rasa parrot project to parrot back.
See docs/rasa-parrot.md for more information
"""

import requests
from dialoguekit.agent.agent import Agent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.intent import Intent


class MovieBotAgent(Agent):
    """Rasa Parrot agent."""

    def __init__(self, agent_id: str):
        """Initializes agent.

        Args:
            agent_id: Agent id.
        """
        super().__init__(agent_id)
        self._MOVIEBOT_URI = "http://152.94.138.15:5001"  # Telegram address
        self._MOVIEBOT_URI = "http://127.0.0.1:5001"  # Messenger address

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
        print(r)  # TODO problem with response here
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
        print(r)  # TODO problem with response here
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
