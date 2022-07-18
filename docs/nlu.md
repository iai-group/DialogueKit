# Natural Language Understanding (NLU)

## Intent Classification

Thus far, two different NLU pipelines are implemented for intent classification

* [Cosine intent classifier](https://github.com/iai-group/dialoguekit/blob/main/dialoguekit/nlu/models/intent_classifier_cosine.py)
* [Rasa DIET classifier](https://github.com/iai-group/dialoguekit/blob/main/dialoguekit/nlu/models/diet_classifier_rasa.py)

An explanation of the implementation of Rasa DIET classifier can be read [here](docs/rasa_component_library.md)

## Entity Extraction

As of now, only one implementation exists, the Rasa DIET classifier.