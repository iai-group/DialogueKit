"""Interface representing domain knowledge."""

import os
from typing import List

import yaml


class Domain:
    def __init__(self, config_file: str) -> None:
        """Represents domain knowledge.

        The YAML configuration file should contain at least the fields name and
        slot_names.

        Args:
            config_file: Name of YAML config file.

        Raises:
            KeyError: if the configuration does not have the fields name and
              slot_names.
        """
        # TODO Extend to multiple entity types
        # See: https://github.com/iai-group/dialoguekit/issues/43
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, encoding="utf-8") as yaml_file:
            self._config = yaml.load(yaml_file, Loader=yaml.FullLoader)

        if not {"name", "slot_names"}.issubset(self._config):
            raise KeyError(
                "The domain configuration should contain at least the fields "
                "'name' and 'slot_names'."
            )

        self._name = self._config.get("name")

    def get_slot_names(self) -> List[str]:
        """Returns the list of slot names.

        Returns:
            List of slot names.
        """
        return list(self._config.get("slot_names").keys())

    def get_name(self) -> str:
        """Returns the name of the domain."""
        return self._name
