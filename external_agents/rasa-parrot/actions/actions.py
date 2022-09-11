"""Rasa parrot agent custom actions.

This files contains your custom actions which can be used to run custom Python
code.

See this guide on how to implement these action:
https://rasa.com/docs/rasa/custom-actions
"""
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionParrot(Action):
    def name(self) -> Text:
        """Name of the action.

        Returns:
            The actions name.
        """
        return "action_parrot"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Action_parrot runner.

        Args:
            dispatcher: Rasa dispatcher.
            tracker: Rasa tracker.
            domain: Rasa domain.

        Returns:
            Runners return statement.
        """
        dispatcher.utter_message(
            text=tracker.latest_message.get("text", "I respond!")
        )

        return []


class ActionStopParrot(Action):
    def name(self) -> Text:
        """Name of the action.

        Returns:
            The actions name.
        """
        return "action_stop"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Action_stop runner.

        Args:
            dispatcher: Rasa dispatcher.
            tracker: Rasa tracker.
            domain: Rasa domain.

        Returns:
            Runners return statement.
        """
        return []
