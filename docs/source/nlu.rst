Natural Language Understanding (NLU)
====================================

The NLU component is responsible for obtaining a structured representation of text utterances. Currently, it entails dialogue acts recognition, key-value annotation (e.g., user sentiment), and user satisfaction prediction.

Dialogue Acts Recognition
-------------------------

A dialogue act is a semantic unit that comprises a single intent and slot-value pairs; an utterance can have multiple dialogue acts. The task of dialogue act recognition can be seen as a combination of intent classification and slot filling. These subtasks can be performed jointly or disjointly. DialogueKit is designed to support both approaches, see base classes: :py:mod:`dialoguekit.nlu.dialogue_acts_extractor.DialogueActsExtractor` and :py:mod:`dialoguekit.nlu.disjoint_dialogue_act_extractor.DisjointDialogueActExtractor`.

Disjoint Dialogue Act Recognition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this component, the task of intent classification and slot filling are performed in a disjoint manner. That is, the intent classifier predicts the intent of the utterance, while the slot filler predicts the slot-value pairs in the utterance. These are then combined to form one dialogue act.

Intent Classification
"""""""""""""""""""""

Thus far two different NLU pipelines are implemented for intent classification.

* Cosine intent classifier :py:mod:`dialoguekit.nlu.models.intent_classifier_cosine`

* Rasa DIET classifier :py:mod:`dialoguekit.nlu.models.diet_classifier_rasa`

See below for details on how the Rasa DIET classifier is used in our implementation.

**Rasa as a component library**

:py:class:`dialoguekit.nlu.models.diet_classifier_rasa.IntentClassifierRasa` implement Rasa's DIET classifier. This is a Dual Intent and Entity Transformer, their paper can be read 
`here. <https://arxiv.org/pdf/2004.09936.pdf>`_

Normally, one would use Rasa as the underlying platform. Here, instead, we use it as a component in DialogueKit. Rasa is distributed with a Apache 2.0 license, granting us free use.

*General idea*


In general, the idea is to import the necessary packages and re-implement the Rasa workflow with their components and structures. 
However, because of how Rasa is structured, DialogueKit objects need to be transformed to Rasa components before use.

*Implementation*

The implementation is in :py:mod:`dialoguekit.nlu.models.diet_classifier_rasa`; this model can be trained and thus uses multiple Rasa components and structures.
Below is a list of all the Rasa imports that are used.

.. code-block:: python

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

Slot Filling
""""""""""""

As of now only one implementation exists, the Rasa DIET classifier.

User Satisfaction Prediction
----------------------------

User satisfaction prediction entails the task of predicting a user's satisfaction with the system, based on the conversation.
We model this as a classification task, where, given the previous *n* user-agent turns, the task of the classifier is to predict the user satisfaction on a scale from 1-5:

#. Very dissatisfied
#. Dissatisfied
#. Normal
#. Satisfied
#. Very satisfied

The current satisfaction classifier is a SVM model pre-trained on `english data <https://github.com/sunnweiwei/user-satisfaction-simulation>`_.