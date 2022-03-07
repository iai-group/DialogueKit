"""Abstract interface for intent classification.

This interface assumes a single intent per utterance, i.a., approaches the
task as a single-label classification problem.
The generalization to multi-label classification is left to future work."""

from typing import Any, Dict, List, Text, Type, Optional
from pathlib import Path
import tempfile
import copy

from dialoguekit.core.utterance import Utterance
from dialoguekit.core.intent import Intent
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation
from dialoguekit.nlu.intent_classifier import IntentClassifier
from dialoguekit.utils.annotation_converter_dialoguekit_to_rasa import (
    AnnotationConverterRasa,
)

# Rasa imports
from rasa.engine.graph import ExecutionContext, GraphComponent, GraphSchema
from rasa.shared.nlu.constants import TEXT
from rasa.nlu.featurizers.sparse_featurizer.count_vectors_featurizer import (
    CountVectorsFeaturizer,
)
from rasa.shared.nlu.training_data.message import Message
from rasa.engine.storage.resource import Resource
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from rasa.engine.storage.local_model_storage import LocalModelStorage
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.classifiers.diet_classifier import DIETClassifier
from rasa.shared.importers.rasa import RasaFileImporter


class IntentClassifierRasa(IntentClassifier):
    def __init__(
        self,
        intents: List[Intent],
        traning_data_path: Optional[str] = "",
        model_path: Optional[
            str
        ] = "/Users/aleksanderdrzewiecki/Documents/GitHub/dialoguekit/.rasa/",
    ) -> None:
        """Initializes the intent classifier.

        Args:
            intents: List of allowed intents.
            model_path Optional[str]: path to where rasa trained model
                                        will be stored.
        """
        self._intents = {i.label: i for i in intents}
        self.model_path = Path(model_path)
        self.def_model_storage = LocalModelStorage.create(self.model_path)
        self.def_resource = Resource(name="rasa_diet_resource")

        self.training_data = None

        self.traning_data_path = traning_data_path
        self.init_pipeline()

    def init_pipeline(self) -> None:
        pipeline = [
            {"component": WhitespaceTokenizer},
            {"component": CountVectorsFeaturizer},
        ]
        if isinstance(self.traning_data_path, str):
            importer = RasaFileImporter(
                training_data_paths=[self.traning_data_path]
            )
            self.training_data: TrainingData = importer.get_nlu_data()
        else:
            raise TypeError("Provided 'traning_data_path' is not a string!")

        self.component_pipeline = [
            self.create_component(
                component.pop("component"),
                component,
                idx,
                model_storage=self.def_model_storage,
            )
            for idx, component in enumerate(copy.deepcopy(pipeline))
        ]

        for component in self.component_pipeline:
            if hasattr(component, "train"):
                component.train(self.training_data)
            if hasattr(component, "process_training_data"):
                component.process_training_data(self.training_data)

        self.diet = DIETClassifier.create(
            {**DIETClassifier.get_default_config()},
            model_storage=self.def_model_storage,
            execution_context=ExecutionContext(
                GraphSchema({}), node_name="diet_1"
            ),
            resource=self.def_resource,
        )
        self.processes_utterances = {}

    def train_model(
        self,
        utterances: Optional[List[Utterance]] = None,
        labels: Optional[List[Intent]] = None,
    ) -> None:
        """Trains a model based on a set of labeled utterances.

        If no utterances or labels are provided 'traning_data_path'
        in the init is used for training the model.
        the utterances and labels are used for creating a rasa nlu
        document. Which then gets used for the training.

        Args:
            utterances: List of Utterance instances.
            labels: List of associated intent labels.

        """
        if utterances and labels:
            # Makes sure we have matching labels for all training utterances.
            assert len(utterances) == len(labels)

            converter = AnnotationConverterRasa(
                save_to_path=tempfile.gettempdir() + "/"
            )
            rasa_file = converter.dialoguekit_to_rasa(
                utterances=utterances, intents=labels
            )
            self.traning_data_path = rasa_file
            self.init_pipeline()

        self._labels = labels
        self.diet.train(self.training_data)

    def get_intent(self, utterance: Utterance) -> Intent:
        """Classifies the intent of an utterance.

        The utterance gets transformed to a Rasa Message before being
        classified. If the utterance has already been processed a cache is used.
        Since DIET also exctracts entities the cache is used if the same
        Classifier object is used.

        Args:
            utterance: An utterance.

        Returns:
            Intent: Predicted intent.

        """
        # Check if utterance is in the processed cache
        if self.processes_utterances.get(utterance.text, None) is None:
            message_text = utterance.text
            message = Message(data={TEXT: message_text})
            message = self.process_message(
                self.component_pipeline, message=message
            )

            classified_message = self.diet.process([message])[0]

            # Add to cache
            self.processes_utterances[
                classified_message.data["text"]
            ] = classified_message

        found_intent = self.processes_utterances.get(utterance.text).data[
            "intent"
        ]["name"]
        if found_intent in self._intents.keys():
            return self._intents[found_intent]
        else:
            return None

    def get_entities(self, utterance: Utterance) -> List[SlotValueAnnotation]:
        """Entity extracion using rasa DIET classifier

        Extracts entities using rasa DIET. Since this model
        does both intent classification and entity extraction,
        the cache is used if the same Utterance has been
        processes before.


        Args:
            utterance (Utterance): User utterance

        Returns:
            List[SlotValueAnnotation]: List of extracted entities
        """
        if self.processes_utterances.get(utterance.text, None) is not None:
            message_text = utterance.text
            message = Message(data={TEXT: message_text})
            message = self.process_message(
                self.component_pipeline, message=message
            )

            classified_message = self.diet.process([message])[0]

            # Add to cache
            self.processes_utterances[
                classified_message.data["text"]
            ] = classified_message

        entities = self.processes_utterances.get(utterance.text).data[
            "entities"
        ]
        slot_value_annotation = [
            SlotValueAnnotation(
                slot=found_entity["entity"],
                value=found_entity["value"],
                start=found_entity["start"],
                end=found_entity["end"],
            )
            for found_entity in entities
        ]
        return slot_value_annotation

    def create_component(
        self,
        component_class: Type[GraphComponent],
        config: Dict[Text, Any],
        idx: int,
        model_storage: LocalModelStorage,
    ) -> GraphComponent:
        """Creates a Rasa pipeline component

        Args:
            component_class (Type[GraphComponent]):
            config (Dict[Text, Any]): component configuration
            idx (int): id of component in pipeline
            model_storage (LocalModelStorage): pipeline component storage

        Returns:
            GraphComponent: The pipeline component
        """
        node_name = f"{component_class.__name__}_{idx}"
        print(node_name)
        execution_context = ExecutionContext(
            GraphSchema({}), node_name=node_name
        )
        resource = Resource(node_name)
        return component_class.create(
            {**component_class.get_default_config(), **config},
            model_storage=model_storage,
            resource=resource,
            execution_context=execution_context,
        )

    def process_message(
        self, loaded_pipeline: List[GraphComponent], message: Message
    ) -> Message:
        """Process a Rasa Message through a pipeline

        Args:
            loaded_pipeline (List[GraphComponent]): Rasa pipeline
            message (Message): Rasa message(utterance)

        Returns:
            Message: processed message with data
        """
        for component in loaded_pipeline:
            component.process([message])

        return message

    def save_model(self, file_path: str) -> None:
        """Saves the trained model to a file.

        Args:
            file_path: File path.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError("Rasa Diet")

    def load_model(self, file_path: str) -> None:
        """Loads a model from a file.

        Args:
            file_path: File path.

        Raises:
            NotImplementedError: If not implemented in derived class.
        """
        raise NotImplementedError
