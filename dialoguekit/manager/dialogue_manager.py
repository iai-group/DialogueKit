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
from dialoguekit.user.user import User
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
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
        self.__dialogue_history = Dialogue(agent.id, user.id)

    @property
    def dialogue_history(self):
        return self.__dialogue_history

    def register_user_utterance(self, utterance: AnnotatedUtterance) -> None:
        """Registers an annotated utterance from the user.

        As the agent is not supposed to have access to the users intent,
        a utterance without the annotation will be sent to the agent.

        Args:
            utterance: User utterance.
        """
        self.__dialogue_history.add_user_utterance(utterance)
        self.__platform.display_user_utterance(utterance)
        self.__agent.receive_user_utterance(utterance.utterance)

    def register_agent_utterance(self, utterance: AnnotatedUtterance) -> None:
        """Registers an annotated utterance from the agent.

        As the user is not supposed to have access to the agents intent,
        a utterance without the annotation will be sent to the user.

        If the Intent label is 'EXIT' the dialoguemanager will close. Thus it is
        only the agent that can close the dialoguemanager.

        Args:
            utterance: Agent utterance.
        """
        self.__dialogue_history.add_agent_utterance(utterance)
        self.__platform.display_agent_utterance(utterance)
        # TODO: Replace with appropriate intent (make sure all intent schemes
        # have an EXIT intent.)
        if utterance.intent is None:
            self.__user.receive_utterance(utterance.utterance)
        if utterance.intent is not None and utterance.intent.label != "EXIT":
            self.__user.receive_utterance(utterance.utterance)
        else:
            self.close()

    def start(self) -> None:
        """Starts the conversation."""
        self.__agent.welcome()
        # TODO: Add some error handling (if connecting the user/agent fails)

    def close(self) -> None:
        """Closes the conversation."""
        pass
        # TODO: save dialogue history, subject to config parameters


if __name__ == "__main__":
    from dialoguekit.core.utterance import Utterance
    from dialoguekit.user.user import User
    from dialoguekit.agent.parrot_agent import ParrotAgent

    # Participants
    agent = ParrotAgent("A01")
    user = User("U01")

    platform = Platform()
    dm = DialogueManager(agent, user, platform)

    user.connect_dialogue_manager(dm)
    agent.connect_dialogue_manager(dm)
    dm.start()

    # Send in user utterance
    dm.register_user_utterance(utterance=Utterance("Hi"))

    dm.close()
