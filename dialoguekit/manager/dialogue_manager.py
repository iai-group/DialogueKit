"""Central broker for coordinating the communication between Agent and User.

The DialogueManager is instantiated with an Agent and a User.  These are then
connected with the particular DialogueManager instance by calling their
respective `connect_dialogue_manager()` methods.

By definition, the communication starts with the Agent's welcome message.
Each agent/user utterance is sent to the other party via their respective
`receive_utterance()` methods.
It is left to to specific Agent and User instances when and how they respond.
It is expected that most will respond immediately upon receiving an utterance,
but this is not required.  Whenever there is a message from either the Agent or
the User, the DialogueManager sends it to the other party by calling their
`receive_{agent/user}_utterance()` method.
"""

from dialoguekit.agent.agent import Agent
from dialoguekit.agent.parrot_agent import ParrotAgent
from dialoguekit.user.user import User
from dialoguekit.core.utterance import Utterance, UtteranceType
from dialoguekit.core.dialogue import Dialogue
from dialoguekit.platform.platform import Platform


class DialogueManager:
    """Represents a dialogue manager."""

    def __init__(self, agent: Agent, user: User, platform: Platform) -> None:
        """Initializes the Dialogue Manager.

        Args:
            agent: An instance of Agent.
            user: An instance of User.
            platform: An instance of Platform.
        """
        self.__agent = agent
        self.__agent.connect_dialogue_manager(self)
        self.__user = user
        self.__user.connect_dialogue_manager(self)
        self.__platform = platform
        self.__dialogue_history = Dialogue(agent.agent_id, user.user_id)

    @property
    def dialogue_history(self):
        return self.__dialogue_history

    def register_user_utterance(self, utterance: Utterance) -> None:
        """Registers an utterance from the user.

        Args:
            utterance: User utterance.
        """
        self.__dialogue_history.add_user_utterance(utterance)
        self.__platform.display_user_utterance(utterance)
        # TODO: This is temp; should be moved to ParrotAgent.
        # Also, termination should be solved more generally.
        if utterance.text == "bye":
            self.__agent.goodbye()
        else:
            self.__agent.receive_user_utterance(utterance)

    def register_agent_utterance(self, utterance: Utterance) -> None:
        """Registers an utterance from the agent.

        Args:
            utterance: Agent utterance.
        """
        self.__dialogue_history.add_agent_utterance(utterance)
        self.__platform.display_agent_utterance(utterance)
        if utterance.utterance_type != UtteranceType.EXIT:
            self.__user.receive_agent_utterance(utterance)

    def start(self) -> None:
        """Starts the conversation."""
        self.__agent.welcome()
        # TODO: Add some error handling (if connecting the user/agent fails)

    def close(self) -> None:
        """Closes the conversation."""
        pass
        # TODO: save dialogue history, subject to config parameters


if __name__ == "__main__":
    agent = ParrotAgent("A01")
    user = User("U01")
    platform = Platform()
    dm = DialogueManager(agent, user, platform)
    dm.start()
    dm.close()
