import json
import yaml
from collections import defaultdict
from yaml.representer import SafeRepresenter
from yaml.nodes import ScalarNode
from typing import Optional, Dict, List

from dialoguekit.utils.annotation_converter import AnnotationConverter


class AnnotationConverterRasa(AnnotationConverter):
    def __init__(
        self, filepath: str, save_to_path: Optional[str] = None
    ) -> None:
        super().__init__(filepath, save_to_path)
        self._intent_examples = {"USER": {}, "AGENT": {}}
        self._slot_value_pairs = defaultdict(set)
        self._data = {}

    def read_original(self) -> None:
        f = open(self._filepath)
        data = json.load(f)
        self._data["original"] = data

        for conversation in data:
            for turn in conversation["conversation"]:
                intent = turn.get("intent", None)
                slot_values = turn.get("slot_values", [])
                utterance = turn.get("utterance", "").strip()
                if len(slot_values) > 0:
                    # Utterance with annotation
                    turn["utterance_annotated"] = utterance
                    for pair in slot_values:
                        turn["utterance_annotated"] = turn[
                            "utterance_annotated"
                        ].replace(pair[1], "[{}]({})".format(pair[1], pair[0]))

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
        """Generates 4 coversions of DialogueKit to Rasa compatible files.

        The generated files are saved in the self._save_to_path.

        Genereted files:
            1. <originalname>_reformat.yml
                The original file saved as a yml

            2. <originalname>_types_w_examples.yml
                The entity types with the corresponding entities identified in
                the text. Used to debug and give an overview

            3. <originalname>_rasa_user.yml
                Conversion of the annotation file to a rasa nlu doc.
                This file represents the USER utterances with intents

            4. <originalname>_rasa_agent.yml
                Conversion of the annotation file to a rasa nlu doc.
                This file represents the AGENT utterances with intents

        Returns:
            Dict[str,str]: Filename, path to file
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

        # Save original as yml
        extention = "_reformat.yml"
        filename = save_name_base + extention
        return_dictionary[filename] = save_path_name + extention
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(self._data["original"], outfile, default_flow_style=False)

        # Save the intent types with examples
        extention = "_types_w_examples.yml"
        filename = save_name_base + extention
        return_dictionary[filename] = save_path_name + extention
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(self._slot_value_pairs, outfile, default_flow_style=False)

        # Used for yml formating
        class LiteralString(str):
            pass

        def change_style(style: str, representer: ScalarNode):
            """Used to change the python yml data representation

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

        def rasa_string(v: List[str]) -> str:
            formated_string = LiteralString(
                "".join(["- " + s.strip() + "\n" for i, s in enumerate(v)])
            )
            return formated_string

        # Create dict with rasa compatible format
        rasa_dict_user = {"version": "3.0", "nlu": []}
        rasa_dict_agent = {"version": "3.0", "nlu": []}
        for k, v in self._intent_examples["USER"].items():
            formated_dict = {"intent": k, "examples": rasa_string(v)}
            rasa_dict_user["nlu"].append(formated_dict)

        for k, v in self._intent_examples["AGENT"].items():
            formated_dict = {"intent": k, "examples": rasa_string(v)}
            rasa_dict_agent["nlu"].append(formated_dict)

        # Save rasa compatible format
        extention = "_rasa_user.yml"
        filename = save_name_base + extention
        return_dictionary[filename] = save_path_name + extention
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(rasa_dict_user, outfile, default_flow_style=False)

        extention = "_rasa_agent.yml.yml"
        filename = save_name_base + extention
        return_dictionary[filename] = save_path_name + extention
        with open(return_dictionary[filename], "w") as outfile:
            yaml.dump(rasa_dict_agent, outfile, default_flow_style=False)

        return return_dictionary


if __name__ == "__main__":
    converter = AnnotationConverterRasa(
        filepath="/Users/aleksanderdrzewiecki/Documents/GitHub/"
        + "dialoguekit/moviebot/annotated_dialogues.json",
        save_to_path="/Users/aleksanderdrzewiecki/Documents/GitHub/"
        "dialoguekit/testing/",
    )
    converter.read_original()
    converter.run()
