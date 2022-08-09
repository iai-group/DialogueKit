Natural Language Understanding (NLU)
====================================

Intent Classification
---------------------

Thus far two different NLU pipelines are implemented for intent classification

* Cosine intent classifier :py:mod:`dialoguekit.nlu.intent_classifier_cosine`

* Rasa DIET classifier :py:mod:`dialoguekit.nlu.diet_classifier_rasa`

An explanation of the implementation of Rasa DIET classifier can be read


Rasa as a component library
^^^^^^^^^^^^^^^^^^^^^^^^^^^

*diet_classifier_rasa* implement Rasa´s DIET classifier. This is a Dual Intent and Entity Transformer, their paper can be read 
`here. <https://arxiv.org/pdf/2004.09936.pdf>`_

Normally one would use Rasa as the underlying platform. But for our use-case we need to use it as a component in Dialoguekit. This proved to be possible with a bit of effort. Rasa is distributed with a Apache 2.0 license, granting us free use.

General idea
""""""""""""

In general the idea was to import the necessary packages and re-implement the rasa workflow with their components and structures. Rasa is built in a very object oriented structure. This does not allow us to use Dialoguekit objects, they need to be transformed to Rasa components before use.

How we implemented it
"""""""""""""""""""""

As stated by a author on medium (link will be updated), the general structure of Rasa is a hard one to understand at first, but after a lot of trial and error we found the best way to get what we needed was to look at the implementation of the tests. They often show a minimal way of using the components separately and in conjunction with each other

The result
""""""""""

The first rasa implementation is in *diet_classifier_rasa*, this model can be trained and thus uses multiple rasa components and structures.
Below you can see all the imports that are used, only from rasa.

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