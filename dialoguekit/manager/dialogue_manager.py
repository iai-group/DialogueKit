"""Dialogue Manager connecting an Agent with an User.

The Dialogue Manager listens to both to ensure that there could be multiple
utterances from either the Agent or the User before the other responds.
"""

from dialoguekit.agent.agent import Agent
from dialoguekit.user.user import User
from dialoguekit.utterance.utterance import Utterance, UtteranceType


class DialogueManager:

    def __init__(self, agent: Agent, user: User) -> None:
        self.__agent = agent
        self.__agent.register_agent(self)
        self.__user = user
        self.__user.register_user(self)
        self.__history = None
        self.__last_user_utterance = None

    def register_agent(self, agent) -> None:
        self.__agent = agent

    def register_user(self, user) -> None:
        self.__user = user

    def register_user_utterance(self, utterance: Utterance):
        print(f"USER:  {utterance.text}")
        if utterance.text == "exit":
            self.__agent.exit()
        else:
            self.__agent.receive_utterance(utterance)

    def register_agent_utterance(self, utterance: Utterance):
        print(f"AGENT: {utterance.text}")
        if utterance.utterance_type != UtteranceType.EXIT:
            self.__user.receive_utterance(utterance)

    def run(self) -> None:
        self.__agent.welcome()

        # while True:  # TODO: add termination criteria
        #
        #     # Give priority to user
        #     if user.take_initiative():
        #         pass
        #     elif user.reply()


if __name__ == "__main__":
    agent = Agent()
    user = User()
    dm = DialogueManager(agent, user)
    dm.run()