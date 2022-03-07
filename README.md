# DialogueKit

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

We follow the [IAI Python Style Guide](https://github.com/iai-group/styleguide/tree/master/python).

## Main concepts

* Agent
* User
* Utterance
* Dialogue Manager
* Ontology: defines the types of entities and the set of properties ("slots") for each entity type.
* There are two types of annotations
  * Intent: represents the dialogue action.
  * SlotValueAnnotation: slot-value pairs, where a slot refers to an entity or a property in the ontology.
* User preferences: preferences are expressed for specific slot-value pairs, where slots correspond to entities or properties in the ontology.

### Concepts specific to item recommendation scenarios

* Item: an entity with a unique ID, canonical name, and any number of properties (represented as property-value pairs, where properties correspond to ontology classes).
* ItemCollection: a collection of items.
* Ratings: explicit user preferences on items (normalized into [-1,1]).

### Usage example

1. Define agent and user

    ```python
    from dialoguekit.core.utterance import Utterance
    from dialoguekit.user.user import User, UserType
    from dialoguekit.agent.parrot_agent import ParrotAgent

    # Participants
    agent = ParrotAgent("A01")
    user = User("U01")
    ```

2. Create and connect platform and dialogue manager

    ```python
    platform = Platform()
    dm = DialogueManager(agent, user, platform)

    user.connect_dialogue_manager(dm)
    agent.connect_dialogue_manager(dm)
    ```

3. Start conversation

    ```python
      dm.start()

      # Send in user utterance
      dm.register_user_utterance(utterance = Utterance("Hi"))

      dm.close()
    ```

### Natural Language Understanding (NLU)

### Intent classification

Thus far two different nlu pipelines are implemented for intent classification

* intent_classifier_cosine
* diet_classifier_rasa

An explanation of the implementation of diet_classifier_rasa can be read [here](example.com)

## Contributors

Krisztian Balog, Shuo Zhang
