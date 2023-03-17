Natural Language Understanding (NLU)
====================================

The NLU component is responsible for obtaining a structured representation of text utterances. Currently, it entails intent classification, entity recognition, and user satisfaction prediction.

Intent Classification
---------------------

Thus far two different NLU pipelines are implemented for intent classification

* Cosine intent classifier :py:mod:`dialoguekit.nlu.models.intent_classifier_cosine`

* Rasa DIET classifier :py:mod:`dialoguekit.nlu.models.diet_classifier_rasa`

See below for an explanation of the implementation of Rasa DIET classifier.

Rasa as a component library
^^^^^^^^^^^^^^^^^^^^^^^^^^^

*diet_classifier_rasa* implement Rasa's DIET classifier. This is a Dual Intent and Entity Transformer, their paper can be read 
`here. <https://arxiv.org/pdf/2004.09936.pdf>`_

Normally one would use Rasa as the underlying platform. But for our use-case we need to use it as a component in DialogueKit. Rasa is distributed with a Apache 2.0 license, granting us free use.

General idea
""""""""""""

In general the idea was to import the necessary packages and re-implement the Rasa workflow with their components and structures. Rasa is built in a very object oriented structure. This does not allow us to use DialogueKit objects, they need to be transformed to Rasa components before use.

Implementation
""""""""""""""

The implementation is in *diet_classifier_rasa*, this model can be trained and thus uses multiple Rasa components and structures.
Below you can see all the imports that are used, only from Rasa.

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

Entity Extraction
-----------------

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