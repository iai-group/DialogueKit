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

    def register_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Registers an annotated utterance from the user.

        As the agent is not supposed to have access to the users intent,
        a utterance without the annotation will be sent to the agent.

        In most cases the Agent should not know about the Users Intent and
        Annotation-s. But for some usecases this additional information may
        become usefull, depending on the UI etc.
        Thus the complete AnnotatedUtterance will be sent to the Agent. It is
        the Agents responsability to only use the information it is supposed
        to.

        Args:
            utterance: User utterance.
        """
        self.__dialogue_history.add_user_utterance(annotated_utterance)
        self.__platform.display_user_utterance(annotated_utterance)
        self.__agent.receive_user_utterance(annotated_utterance)

    def register_agent_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Registers an annotated utterance from the agent.

        In most cases the User should not know about the Agents Intent and
        Annotation-s. But for some usecases this additional information may
        become usefull, depending on the UI etc.
        Thus the complete AnnotatedUtterance will be sent to the User. It is
        the Users responsability to only use the information it is supposed
        to.

        If the Intent label is 'EXIT' the dialoguemanager will close. Thus it is
        only the agent that can close the dialoguemanager.

        Args:
            utterance: Agent utterance.
        """
        self.__dialogue_history.add_agent_utterance(annotated_utterance)
        self.__platform.display_agent_utterance(annotated_utterance)
        # TODO: Replace with appropriate intent (make sure all intent schemes
        # have an EXIT intent.)
        if (
            annotated_utterance.intent is not None
            and annotated_utterance.intent.label == "EXIT"
        ):
            self.close()
        else:
            self.__user.receive_agent_utterance(annotated_utterance)

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
