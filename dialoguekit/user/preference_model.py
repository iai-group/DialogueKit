from typing import Dict

class PreferenceModel:
    """Representation of the user's preferences."""

    def __init__(self) -> None:
        """Initializes the user's preference model."""
        pass

    def load_db(self) -> None:
        """Loads db/csv file as backend knowledge."""
        pass

    def initialize_preferences(self) -> None:
        """Initializes the user's preferences via sampling items"""
        pass

    def rate_item(self, slots: Dict) -> int:
        """Rates the items"""
        pass

    def next_user_slots(self, agent_intent: str, agent_slot_values: Dict) -> Dict:
        """Determins the next user slots via loading from the inialized preferences or sampling."""
        pass

    def update_preferences(self, agent_slot_values: Dict, rating: int) -> None:
        """Updates user preferences via adding like/disliked items."""
        pass
