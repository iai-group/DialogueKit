import json
import yaml
import time
from collections import defaultdict
from yaml.representer import SafeRepresenter
from yaml.nodes import ScalarNode
from typing import Optional, Dict, List

from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.utils.annotation_converter import AnnotationConverter


# Used for yaml formatting
class LiteralString(str):
    pass


class AnnotationConverterRasa(AnnotationConverter):
    def __init__(
        self, filepath: Optional[str] = "", save_to_path: Optional[str] = None
    ) -> None:
        super().__init__(filepath, save_to_path)
        self._intent_examples = {"USER": {}, "AGENT": {}}
        self._slot_value_pairs = defaultdict(set)
        self._data = {}

    def rasa_string(self, v: List[str]) -> str:
        formatted_string = LiteralString(
            "".join(
                [
                    "- " + s.strip() + "\n"
                    if i > 0
                    else "- " + s.strip() + "\n"
                    for i, s in enumerate(v)
                ]
            )
        )
        return formatted_string

    def change_style(self, style: str, representer: ScalarNode):
        """Used to change the python yaml data representation
        Args:
            style (str): Style used to represent type
            representer (ScalarNode): representer type ->
                        (SafeRepresenter.represent_str)
        """

        def new_representer(dumper, data):
            scalar = representer(dumper, data)
            scalar.style = style
            return scalar

        return new_representer

    def _remove_whitespace(self, utterance_text: str) -> str:
        utterance_text = utterance_text.strip()
        utterance_text = utterance_text.replace("\n", " ")
        return utterance_text

    def read_original(self) -> None:
        f = open(self._filepath)
        data = json.load(f)
        self._data["original"] = data

        for conversation in data:
            for turn in conversation["conversation"]:
                intent = turn.get("intent", None)
                slot_values = turn.get("slot_values", [])
                utterance = self._remove_whitespace(turn.get("utterance", ""))

                if len(slot_values) > 0:
                    turn["utterance_annotated"] = utterance
                    for annotation in slot_values:
                        placeholder_label, value = annotation[0], annotation[1]
                        turn["utterance_annotated"] = turn[
                            "utterance_annotated"
                        ].replace(f"{value}", f"{{{placeholder_label}}}", 1)
                    # Utterance with annotation
                    for pair in slot_values:
                        turn["utterance_annotated"] = turn[
                            "utterance_annotated"
                        ].replace(
                            f"{{{str(pair[0])}}}",
                            "[{}]({})".format(pair[1], pair[0]),
                            1,
                        )

                        # Annotation types with examples
                        self._slot_value_pairs[pair[0]].add(pair[1])

                # Intent with examples
                if intent not in self._intent_examples[turn["participant"]]:
                    self._intent_examples[turn["participant"]][intent] = set()

                self._intent_examples[turn["participant"]][intent].add(
                    turn.get("utterance_annotated", utterance)
                )

        self._slot_value_pairs = {
            k: list(v) for k, v in self._slot_value_pairs.items()
        }
        self._intent_examples = {
            k: {i: list(l) for i, l in v.items()}
            for k, v in self._intent_examples.items()
        }

    def run(self) -> Dict[str, str]:
        """Generates 4 conversions of DialogueKit to Rasa compatible files.

        The generated files are saved in the self._save_to_path.

        Generated files:
            1. <originalname>_reformat.yaml
                The original file saved as a yaml

            2. <originalname>_types_w_examples.yaml
                The entity types with the corresponding entities identified in
                the text. Used to debug and give an overview

            3. <originalname>_rasa_user.yaml
                Conversion of the annotation file to a rasa nlu doc.
                This file represents the USER utterances with intents

            4. <originalname>_rasa_agent.yaml
                Conversion of the annotation file to a rasa nlu doc.
                This file represents the AGENT utterances with intents

        Returns:
            Filename: path to file pairs
        """

        if len(self._slot_value_pairs.values()) <= 0:
            raise TypeError(
                "Your need to use the read_original() "
                "function before running run()"
            )

        return_dictionary = {}
        save_path_name = (
            self._save_to_path + self._filepath.split("/")[-1].split(".")[-2]
        )
        save_name_base = self._filepath.split("/")[-1].split(".")[-2]

        # Save original as yaml
        extension = "_reformat.yaml"
        filename = save_name_base + extension
        return_dictionary[filename] = save_path_name + extension
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(self._data["original"], outfile, default_flow_style=False)

        # Save the intent types with examples
        extension = "_types_w_examples.yaml"
        filename = save_name_base + extension
        return_dictionary[filename] = save_path_name + extension
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(self._slot_value_pairs, outfile, default_flow_style=False)

        def change_style(style: str, representer: ScalarNode):
            """Used to change the python yaml data representation

            Args:
                style (str): Style used to represent type
                representer (ScalarNode): representer type ->
                            (SafeRepresenter.represent_str)
            """

            def new_representer(dumper, data):
                scalar = representer(dumper, data)
                scalar.style = style
                return scalar

            return new_representer

        represent_literal_list = change_style(
            "|", SafeRepresenter.represent_str
        )
        yaml.add_representer(LiteralString, represent_literal_list)

        # Create dict with rasa compatible format
        rasa_dict_user = {"version": "3.0", "nlu": []}
        rasa_dict_agent = {"version": "3.0", "nlu": []}
        for k, v in self._intent_examples["USER"].items():
            formatted_dict = {"intent": k, "examples": self.rasa_string(v)}
            rasa_dict_user["nlu"].append(formatted_dict)

        for k, v in self._intent_examples["AGENT"].items():
            formatted_dict = {"intent": k, "examples": self.rasa_string(v)}
            rasa_dict_agent["nlu"].append(formatted_dict)

        # Save rasa compatible format
        extension = "_rasa_user.yaml"
        filename = save_name_base + extension
        return_dictionary[filename] = save_path_name + extension
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(rasa_dict_user, outfile, default_flow_style=False)

        extension = "_rasa_agent.yaml"
        filename = save_name_base + extension
        return_dictionary[filename] = save_path_name + extension
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(rasa_dict_agent, outfile, default_flow_style=False)

        return return_dictionary

    def dialoguekit_to_rasa(
        self, utterances: List[Utterance], intents: List[Intent]
    ) -> str:

        rasa_dict = {"version": "3.0", "nlu": []}
        for u, i in zip(utterances, intents):
            formatted_dict = {
                "intent": i.label,
                "examples": self.rasa_string([u.text]),
            }
            rasa_dict["nlu"].append(formatted_dict)

        represent_literal_list = self.change_style(
            "|", SafeRepresenter.represent_str
        )
        yaml.add_representer(LiteralString, represent_literal_list)
        # Save rasa compatible format
        filepath = (
            self._save_to_path + "_" + str(int(time.time())) + "_rasa.yaml"
        )
        with open(filepath, "w") as outfile:
            yaml.dump(rasa_dict, outfile, default_flow_style=False)

        return filepath


if __name__ == "__main__":
    converter = AnnotationConverterRasa(
        filepath="/Users/aleksanderdrzewiecki/Documents/GitHub/"
        + "dialoguekit/moviebot/annotated_dialogues.json",
        save_to_path="/Users/aleksanderdrzewiecki/Documents/GitHub/"
        "dialoguekit/testing/",
    )
    converter.read_original()
    converter.run()
