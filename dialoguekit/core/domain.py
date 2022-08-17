"""Interface representing domain knowledge."""

import os
from typing import List

import yaml


class Domain:
    def __init__(self, config_file: str) -> None:
        """Represents domain knowledge.

        Args:
            config_file: Name of YAML config file.
        """
        # TODO Extend to multiple entity types
        # See: https://github.com/iai-group/dialoguekit/issues/43
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")
        with open(config_file) as yaml_file:
            self._config = yaml.load(yaml_file, Loader=yaml.FullLoader)

    def get_slot_names(self) -> List[str]:
        """Returns the list of slot names.

        Returns:
            List of slot names.
        """
        return list(self._config["slot_names"].keys())
