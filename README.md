# DialogueKit

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

We follow the [IAI Python Style Guide](https://github.com/iai-group/styleguide/tree/master/python).

## Main concepts

* **Participant**
  * **User** and **Agent** are Participants
  * Represents a participant is the conversation.
* **Agent**
  * Represents a bot, with its own set of logic, NLU and NLG.
* **User**
  * Represents a human interacting. Has the simplest form of interaction, which are strings to and from the **Dialogue Manager**.
* Utterance
  * An utterance by an **Agent** or **User**. The utterance holds the participant utterance as clear text and can hold additionally to the intent and or annotation.
* Platform
  * The platform is the way the participants communicate with each other. This can be native to DialogueKit or other forms as REST APIs or other methods.
* Dialogue Manager
  * Holds and orchestrates the conversation between the participants.
* Ontology
  * Defines the types of entities and the set of properties ("slots") for each entity type.
* There are two types of annotations
  * Intent: represents the dialogue action.
  * SlotValueAnnotation: slot-value pairs, where a slot refers to an entity or a property in the ontology.
* User preferences
  * Preferences are expressed for specific slot-value pairs, where slots correspond to entities or properties in the ontology.

### Concepts specific to item recommendation scenarios

* Item: an entity with a unique ID, canonical name, and any number of properties (represented as property-value pairs, where properties correspond to ontology classes).
* ItemCollection: a collection of items.
* Ratings: explicit user preferences on items (normalized into [-1,1]).

### Usage example

**NOTE (TODO):** This usage example will shortly be outdated as of issue [#58.](https://github.com/iai-group/dialoguekit/issues/58)

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

#### Intent Classification

Thus far two different NLU pipelines are implemented for intent classification

* [Cosine intent classifier](https://github.com/iai-group/dialoguekit/blob/main/dialoguekit/nlu/models/intent_classifier_cosine.py)
* Rasa DIET classifier (TODO: Add link after merge)

An explanation of the implementation of Rasa DIET classifier can be read [here](docs/rasa_component_library.md)

#### Entity Extraction

As of now only one implementation exists, the Rasa DIET classifier.

## Contributors

Jafar Afzali, Krisztian Balog, Aleksander Drzewiecki and Shuo Zhang
