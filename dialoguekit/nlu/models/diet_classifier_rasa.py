"""Rasa DIET classifier.

More information about the DIET classifier
https://rasa.com/docs/rasa/reference/rasa/nlu/classifiers/diet_classifier/

A short description of how we use Rasa as a component library can be seen inn
the docs/rasa_component_library.md
"""

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
        model_path: Optional[str] = ".rasa",
    ) -> None:
        """Initializes the intent classifier.

        The traning data path may be used with a Rasa nlu.yml file. It is also
        possible to use the self.train_model function with a list of Utterance
        and a list of Intent.

        Args:
            intents: List of allowed intents.
            traning_data_path Optional[str]: path to the traning data yml.
            model_path Optional[str]: path to where rasa trained model will be
                                        stored.
        """
        self._intents = {i.label: i for i in intents}
        self._model_path = Path(model_path)
        self._def_model_storage = LocalModelStorage.create(self._model_path)
        self._def_resource = Resource(name="rasa_diet_resource")

        self._training_data = None

        self._traning_data_path = traning_data_path
        self.init_pipeline()

    def init_pipeline(self) -> None:
        """Creates classifier and initialize.

        A component pipeline of Rasa components gets created and initialized.
        The DIET classifier object then gets created with the pipeline.

        Raises:
            TypeError if traning_data_path is not a string
        """
        pipeline = [
            {"component": WhitespaceTokenizer},
            {"component": CountVectorsFeaturizer},
        ]
        if isinstance(self._traning_data_path, str):
            importer = RasaFileImporter(
                training_data_paths=[self._traning_data_path]
            )
            self._training_data: TrainingData = importer.get_nlu_data()
        else:
            raise TypeError("Provided 'traning_data_path' is not a string!")

        self._component_pipeline = [
            self.create_component(
                component.pop("component"),
                component,
                idx,
                model_storage=self._def_model_storage,
            )
            for idx, component in enumerate(copy.deepcopy(pipeline))
        ]

        for component in self._component_pipeline:
            if hasattr(component, "train"):
                component.train(self._training_data)
            if hasattr(component, "process_training_data"):
                component.process_training_data(self._training_data)

        self._diet = DIETClassifier.create(
            {**DIETClassifier.get_default_config()},
            model_storage=self._def_model_storage,
            execution_context=ExecutionContext(
                GraphSchema({}), node_name="diet_1"
            ),
            resource=self._def_resource,
        )
        self._processes_utterances = {}

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
            self._traning_data_path = rasa_file
            self.init_pipeline()

        self._labels = labels
        self._diet.train(self._training_data)

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
        self.process_utterance(utterance=utterance)

        found_intent = self._processes_utterances.get(utterance.text).data[
            "intent"
        ]["name"]
        return self._intents.get(found_intent, None)

    def get_annotations(
        self, utterance: Utterance
    ) -> List[SlotValueAnnotation]:
        """Entity extracion using rasa DIET classifier.

        Extracts entities using rasa DIET. Since this model
        does both intent classification and entity extraction,
        the cache is used if the same Utterance has been
        processes before.


        Args:
            utterance (Utterance): User utterance

        Returns:
            List[SlotValueAnnotation]: List of extracted entities
        """
        self.process_utterance(utterance=utterance)

        entities = self._processes_utterances.get(utterance.text).data[
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
        """Creates a Rasa pipeline component.

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

    def process_utterance(self, utterance: Utterance) -> None:
        """Processes utterance and adds to cache.

        If it is the first time this utterance is processed it gets added to
        the cache. Next time the same utterance wants to get processed it gets
        skipped, as its processing result is in the cache.

        Args:
            utterance: Agent or User Utterance
        """
        if utterance.text not in self._processes_utterances:
            message_text = utterance.text
            message = Message(data={TEXT: message_text})
            message = self.process_message(
                self._component_pipeline, message=message
            )

            classified_message = self._diet.process([message])[0]

            # Add to cache
            self._processes_utterances[
                classified_message.data["text"]
            ] = classified_message

    def process_message(
        self, loaded_pipeline: List[GraphComponent], message: Message
    ) -> Message:
        """Processes a Rasa Message through a pipeline.

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
