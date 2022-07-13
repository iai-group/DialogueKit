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
import os
import json
import calendar
import datetime
from dialoguekit.agent.agent import Agent
from dialoguekit.user.user import User
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.dialogue import Dialogue
from dialoguekit.platforms.platform import Platform

_DIALOGUE_EXPORT_PATH = "dialogue_export"


class DialogueManager:
    """Represents a dialogue manager."""

    def __init__(
        self,
        agent: Agent,
        user: User,
        platform: Platform,
        save_dialogue_history: bool = True,
    ) -> None:
        """Initializes the Dialogue Manager.

        Args:
            agent: An instance of Agent.
            user: An instance of User.
            platform: An instance of Platform.
        """
        self._agent = agent
        self._agent.connect_dialogue_manager(self)
        self._user = user
        self._user.connect_dialogue_manager(self)
        self._platform = platform
        self._dialogue_history = Dialogue(agent.id, user.id)
        self._save_dialogue_history = save_dialogue_history

    @property
    def dialogue_history(self):
        return self._dialogue_history

    def register_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Registers an annotated utterance from the user.

        In most cases the Agent should not know about the Users Intent and
        Annotation-s. But for some usecases this additional information may
        become usefull, depending on the UI etc.
        Thus the complete AnnotatedUtterance will be sent to the Agent. It is
        the Agents responsability to only use the information it is supposed
        to.

        Args:
            utterance: User utterance.
        """
        self._dialogue_history.add_user_utterance(annotated_utterance)
        self._platform.display_user_utterance(annotated_utterance)
        self._agent.receive_user_utterance(annotated_utterance)

    def register_agent_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Registers an annotated utterance from the agent.

        This method takes a AnnotatedUtterance but only a Utterance gets sent to
        the User. The AnnotatedUtterance gets used to store the conversation for
        future reference, and if the Agent wants to end the conversation with
        the "EXIT" Intent, the DialogueMangager will end the conversation with
        the close() method.

        Note:
            If the Intent label is 'EXIT' the dialoguemanager will close. Thus
            it is only the agent that can close the dialoguemanager.

        Args:
            utterance: Agent utterance.
        """
        self._dialogue_history.add_agent_utterance(annotated_utterance)
        self._platform.display_agent_utterance(annotated_utterance)
        # TODO: Replace with appropriate intent (make sure all intent schemes
        # have an EXIT intent.)
        if annotated_utterance.intent is not None and (
            annotated_utterance.intent.label == "EXIT"
            or annotated_utterance.intent.label == "BYE"
        ):
            self.close()
        else:
            self._user.receive_utterance(annotated_utterance.utterance)

    def start(self) -> None:
        """Starts the conversation."""
        self._agent.welcome()
        # TODO: Add some error handling (if connecting the user/agent fails)

    def close(self) -> None:
        """Closes the conversation.

        If '_save_dialogue_history' is set to True it will export the dialogue
        history.
        """
        if self._save_dialogue_history:
            self._dump_dialogue_history()

    def _dump_dialogue_history(self):
        """Exports the dialogue history.

        The exported files will be named as 'AgentID_UserID.json'

        If the two participants have had a conversation previously, the new
        conversation will be appended to the same export document.
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

        date = datetime.datetime.utcnow()
        utc_time = calendar.timegm(date.utctimetuple())
        run_conversation = {
            "conversation ID": str(utc_time),
            "conversation": [],
            "agent": self._agent.to_dict(),
            "user": self._user.to_dict(),
        }

        for annotated_utterance in history.utterances:
            print(annotated_utterance)

            utterance_info = {
                "participant": annotated_utterance.get("sender").name,
                "utterance": annotated_utterance.get("utterance").text.replace(
                    "\n", ""
                ),
            }

            if annotated_utterance.get("utterance").intent is not None:
                utterance_info["intent"] = annotated_utterance.get(
                    "utterance"
                ).intent.label

            if (
                annotated_utterance.get("utterance").metadata.get(
                    "satisfaction"
                )
                is not None
            ):
                utterance_info["satisfaction"] = annotated_utterance.get(
                    "utterance"
                ).metadata.get("satisfaction")

            annotations = annotated_utterance.get("utterance").get_annotations()
            if annotations:
                slot_values = []
                for annotation in annotations:
                    slot_values.append([annotation.slot, annotation.value])
                utterance_info["slot_values"] = slot_values
            run_conversation["conversation"].append(utterance_info)

        json_file.append(run_conversation)

        with open(file_name, "w") as outfile:
            json.dump(json_file, outfile)

        # Empty dialogue history to avoid duplicate save
        for _ in range(len(self._dialogue_history.utterances)):
            self._dialogue_history.utterances.pop()
        # TODO: save dialogue history, subject to config parameters


if __name__ == "__main__":
    from dialoguekit.user.user_with_intent import UserWithIntent
    from dialoguekit.user.user import User
    from dialoguekit.agent.mathematics_agent import MathAgent
    from dialoguekit.agent.moviebot_agent import MovieBotAgent
    from dialoguekit.agent.woz_agent import WOZAgent
    from dialoguekit.core.intent import Intent

    # Participants
    agent = MathAgent("MA01")
    agent = MovieBotAgent(agent_id="MovieBot01")
    user = UserWithIntent(
        "UI01", intents=[Intent("START"), Intent("ANSWER"), Intent("COMPLETE")]
    )
    user = User(id="TEST01")
    agent = WOZAgent(
        id="WoZ", intent_recommendations=[Intent("EXIT"), Intent("RANDOM")]
    )

    platform = Platform()
    dm = DialogueManager(agent, user, platform)

    user.connect_dialogue_manager(dm)
    agent.connect_dialogue_manager(dm)
    dm.start()

    dm.close()
