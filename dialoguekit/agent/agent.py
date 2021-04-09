"""Abstract class representing core agent functionality.

This parent class is to be used both for bots and human ("Wizard of Oz") agents.
"""

from enum import Enum

#from dialoguekit.manager.dialogue_manager import DialogueManager
from dialoguekit.utterance.utterance import Utterance, UtteranceType


class AgentType(Enum):

    BOT = 0
    WOZ = 1


# TODO: Make it an abstract class and also one simple child class "ParrotAgent"
class Agent:

    def __init__(self) -> None:
        self._agent_type = AgentType.BOT
        self._dm = None

    def register_agent(self, dm) -> None:
        self._dm = dm

    def welcome(self) -> None:
        utterance = Utterance("Hello, I'm Parrot. What can I help u with?", UtteranceType.WELCOME)
        self._dm.register_agent_utterance(utterance)

    def exit(self) -> None:
        utterance = Utterance("It was nice talking to you. Bye", UtteranceType.EXIT)
        self._dm.register_agent_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new user utterance.

        The agent can respond immediately after each utterance or can decide to
        wait -- it is left to the individual agent.
        """
        # sending agent response - repeating what the user said
        response = Utterance("Parrot " + utterance.text)
        self._dm.register_agent_utterance(response)
