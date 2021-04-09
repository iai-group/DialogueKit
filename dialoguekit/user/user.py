from enum import Enum

#import dialoguekit.manager.dialogue_manager
from dialoguekit.utterance.utterance import Utterance

class UserType(Enum):
    HUMAN = 0
    SIMULATOR = 1


class User:

    def __init__(self) -> None:
        self._user_type = UserType.HUMAN
        # TODO(to include)
        # - History
        self._dm = None

    def register_user(self, dm) -> None:
        self._dm = dm

    def receive_utterance(self, utterance: Utterance) -> None:
        """This method is called each time there is a new agent utterance.

        The user can respond immediately after each utterance or can decide to
        wait.
        """
        # sending agent response
        text = input("Your response: ")
        response = Utterance(text)
        self._dm.register_user_utterance(response)

    # def join(self) -> None:
    #     """The user joins the conversation."""
    #     pass
    #
    # def reply(self, agent_utterance: Utterance) -> Utterance:
    #     """Replies to agent utterance."""
    #     pass
    #
    # def take_initiative(self) -> Utterance:
    #     """Takes initiative a send an utterance without waiting for agent utterance."""
    #     pass