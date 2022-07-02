"""Wizard-of-Oz (WoZ) agent.

A WoZ agent is one that is controlled by a human operator. It can be especially
useful for human-human data collection or for testing simulated users.
"""
from typing import List, Optional
from dialoguekit.core.intent import Intent
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.agent.agent import Agent, AgentType


class WOZAgent(Agent):
    """Represents a WoZ agent."""

    def __init__(
        self,
        id: str,
        intent_recommendations: Optional[List[Intent]] = None,
        type: Optional[AgentType] = AgentType.WOZ,
    ) -> None:
        """Initializes the agent.

        If 'intent_recommendations' are provided the WOZAgent will ask the
        operator to explicitly declare the intent of the response, before
        prompting for the text of the utterance.

        Args:
            id: Agent ID.
            intent_recommendations: List of intents the Agent can select from.
            type: Agent type (default: BOT).
        """
        super().__init__(id=id, type=type)
        self._intent_recommendations = intent_recommendations

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        text = input("Your WELCOME message: ")
        response = AnnotatedUtterance(text)
        self._dialogue_manager.register_agent_utterance(response)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        text = input("Your GOODBYE message: ")
        response = AnnotatedUtterance(text, intent=Intent("EXIT"))
        response
        self._dialogue_manager.register_agent_utterance(response)

    def receive_user_utterance(
        self, annotated_utterance: AnnotatedUtterance
    ) -> None:
        """Responds to the user with an AnnotatedUtterance.

        If 'intent_recommendations' are provided the operator of the Agent will
        be asked to declare the response intent. It is possible to declare
        another intent then the ones that are provided in the list by pressing
        ENTER.

        Args:
            annotated_utterance: The users Utterance. Not used by this agent.
        """
        response_intent = None
        if self._intent_recommendations:
            while response_intent is None:
                print(
                    "Select desired INTENT. Press ENTER for writing your own "
                    "INTENT"
                )
                print(
                    ", ".join(
                        [
                            f"{i+1}: {intent.label}"
                            for i, intent in enumerate(
                                self._intent_recommendations
                            )
                        ]
                    )
                )
                response_intent_nr = input("INTENT number: ")
                if len(response_intent_nr) == 0:
                    response_intent_text = input("Write your desired INTENT: ")
                    response_intent = Intent(response_intent_text)
                try:
                    if int(response_intent_nr) in range(
                        1, len(self._intent_recommendations) + 1
                    ):
                        response_intent = self._intent_recommendations[
                            int(response_intent_nr) - 1
                        ]
                except (IndexError, ValueError):
                    pass

        text = input("Your response: ")
        response = AnnotatedUtterance(text, intent=response_intent)
        self._dialogue_manager.register_agent_utterance(response)
