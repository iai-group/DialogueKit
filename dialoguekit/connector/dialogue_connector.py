"""Central broker for coordinating the communication between Agent and User.

The DialogueConnector is instantiated with an Agent and a User.  These are then
connected with the particular DialogueConnector instance by calling their
respective `connect_dialogue_connector()` methods.

By definition, the communication starts with the Agent's welcome message.
Each agent/user utterance is sent to the other party via their respective
`receive_utterance()` methods.
It is left to to specific Agent and User instances when and how they respond.
It is expected that most will respond immediately upon receiving an utterance,
but this is not required.  Whenever there is a message from either the Agent or
the User, the DialogueConnector sends it to the other party by calling their
`receive_{agent/user}_utterance()` method.
"""
import json
import os

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.dialogue import Dialogue
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.user import User
from dialoguekit.platforms.platform import Platform

_DIALOGUE_EXPORT_PATH = "dialogue_export"


class DialogueConnector:
    def __init__(
        self,
        agent: Agent,
        user: User,
        platform: Platform,
        save_dialogue_history: bool = True,
    ) -> None:
        """Represents a dialogue connector.

        Args:
            agent: An instance of Agent.
            user: An instance of User.
            platform: An instance of Platform.
            save_dialogue_history: Flag to save the dialogue or not.
        """
        self._agent = agent
        self._agent.connect_dialogue_connector(self)
        self._user = user
        self._user.connect_dialogue_connector(self)
        self._platform = platform
        self._dialogue_history = Dialogue(agent.id, user.id)
        self._save_dialogue_history = save_dialogue_history

    @property
    def dialogue_history(self):
        """Return the dialogue history."""
        return self._dialogue_history

    def register_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Registers an annotated utterance from the user.

        In most cases the Agent should not know about the Users Intent and
        Annotation-s. But for some use cases this additional information may
        become useful, depending on the UI etc.
        Thus the complete AnnotatedUtterance will be sent to the Agent. It is
        the Agents responsibility to only use the information it is supposed
        to.

        Args:
            annotated_utterance: User utterance.
        """
        self._dialogue_history.add_utterance(annotated_utterance)
        self._platform.display_user_utterance(annotated_utterance)
        self._agent.receive_utterance(annotated_utterance)

    def register_agent_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Registers an annotated utterance from the agent.

        This method takes a AnnotatedUtterance but only a Utterance gets sent to
        the User. The AnnotatedUtterance gets used to store the conversation for
        future reference, and if the Agent wants to end the conversation with
        the _agent.stop_intent Intent, the DialogueConnector will end the
        conversation with the close() method.

        Note:
            If the Intent label is 'EXIT' the DialogueConnector will close. Thus
            it is only the agent that can close the DialogueConnector.

        Args:
            annotated_utterance: Agent utterance.
        """
        self._dialogue_history.add_utterance(annotated_utterance)
        self._platform.display_agent_utterance(annotated_utterance)
        # TODO: Replace with appropriate intent (make sure all intent schemes
        # have an EXIT intent.)
        if annotated_utterance.intent == self._agent.stop_intent:
            self.close()
        else:
            self._user.receive_utterance(annotated_utterance)

    def start(self) -> None:
        """Starts the conversation."""
        self._agent.welcome()
        # TODO: Add some error handling (if connecting the user/agent fails)

    def close(self) -> None:
        """Closes the conversation.

        If '_save_dialogue_history' is set to True it will export the
        dialogue history.
        """
        if self._save_dialogue_history:
            self._dump_dialogue_history()

    def _dump_dialogue_history(self):
        """Exports the dialogue history.

        The exported files will be named as 'AgentID_UserID.json'

        If the two participants have had a conversation previously, the new
        conversation will be appended to the same export document.

        Per dialogue, the dialogue metadata will be added. Also per utterance
        the utterance metadata, will be added to the same level as the utterance
        text. Intent will also be exported if provided.
        """
        # If conversation is empty we do not save it.
        if len(self._dialogue_history.utterances) == 0:
            return

        history = self._dialogue_history
        file_name = (
            f"{_DIALOGUE_EXPORT_PATH}/{self._agent.id}_{self._user.id}.json"
        )
        json_file = []

        # Check directory and read if exists.
        if not os.path.exists(_DIALOGUE_EXPORT_PATH):
            os.makedirs(_DIALOGUE_EXPORT_PATH)
        if os.path.exists(file_name):
            with open(file_name) as json_file_out:
                json_file = json.load(json_file_out)

        dialogue_as_dict = history.to_dict()
        dialogue_as_dict["agent"] = self._agent.to_dict()
        dialogue_as_dict["user"] = self._user.to_dict()

        json_file.append(dialogue_as_dict)

        with open(file_name, "w") as outfile:
            json.dump(json_file, outfile)

        # Empty dialogue history to avoid duplicate save
        for _ in range(len(self._dialogue_history.utterances)):
            self._dialogue_history.utterances.pop()
        # TODO: save dialogue history, subject to config parameters


if __name__ == "__main__":
    from dialoguekit.participant.user import User
    from sample_agents.moviebot_agent import MovieBotAgent

    # Participants
    agent = MovieBotAgent(
        agent_id="MovieBot01", uri="http://152.94.232.43:5001/"
    )
    user = User(id="TEST01")

    platform = Platform()
    dm = DialogueConnector(agent, user, platform)

    user.connect_dialogue_connector(dm)
    agent.connect_dialogue_connector(dm)
    dm.start()

    dm.close()
