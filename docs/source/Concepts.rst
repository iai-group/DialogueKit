
Main concepts
=============

.. image:: _static/DialogueKit-Architecture.png
    :width: 400
    :alt: Image illustrating the connections between DialogueKit´s main concepts.


Participant 
-----------
:py:mod:`dialoguekit.participant.participant`

Represents a participant in the conversation.

* **User** and **Agent** are Participants


Agent
-----
:py:mod:`dialoguekit.agent.agent`

Represents a bot, with its own set of logic, **NLU** and **NLG**.

Agents and users are the participants in a dialog. DialogueKit assumes the
agent to be a conversational system and the user to be a human. However,
users of DialogueKit can change this by implementing a superclass of User.

In a conversation, DialogueKit assumes the Agent to always start the
conversation and also end it. A User can initialize the end of a
conversation, but the responsibility lies on the Agent to stop it.

Out of the box DialogueKit contains some sample agents. These are described
below:

* **ParrotAgent**: This agent will welcome the User, but will always parrot (echo) the User.

* **RasaParrotAgent**: This agent looks like the **ParrotAgent** to the user, but is actually just a connector to a Rasa conversational agent. This conversational agent is also part of DialogueKit

* **MathAgent**: This **Agent** will ask the user simple arithmetic (addition, subtraction, multiplication and division) questions.

* **MovieBotAgent**: A Connector agent for `IAI MovieBot <https://github.com/iai-group/moviebot>`_ .

* **WozAgent**: Allows a real human to interact with a User. This can be useful for testing user simulators.

User 
----
:py:mod:`dialoguekit.user.user`

Represents a human interacting. Has the simplest form of interaction, which are strings to and from the **Dialogue Manager**.


Utterance
---------
:py:mod:`dialoguekit.core.utterance`

An **utterance** by an **Agent** or **User**. The utterance holds the participant utterance as clear text. To store additional information such as intent and or annotation the :py:mod:`dialoguekit.core.annotated_utterance` should be used.

Additionally the **annotated_utterance** can store other user defined metadata. **DialogueKit** uses this metadata field for the **Satisfaction Classifier**. The ``metadata`` field is a dictionary with the structure: ``Dict[str, Any]``.

In our case for satisfaction, the ``metadata`` field looks as follows:

.. code-block:: json

    metadata = {
        "satisfaction": int
    }

This metadata will then be used in the natural language generation. You are free to use ``metadata`` for your own use-cases.


Platform 
--------
:py:mod:`dialoguekit.platforms.platform`

The Platform’s responsibility is to display the conversation. DialogueKit
includes a simple terminal-based platform. However, it can support other
platforms by facilitating communication over POST requests. To avoid
unnecessary complexity, the Platform is limited to only display utterances
from the participants, i.e., user and agent utterances. This approach allows
the DM and the Platform to be as independent of each other as possible and
simplifies the integration of other platforms.


Dialogue Manager 
----------------
:py:mod:`dialoguekit.manager.dialogue_manager`

Holds and orchestrates the conversation between the participants.


Ontology 
--------
:py:mod:`dialoguekit.core.ontology`

Defines the types of entities and the set of properties ("slots") for each entity type.


Annotations
-----------
There are two types of annotations

* **Intent** :py:mod:`dialoguekit.core.intent`: represents the dialogue action.

* **SlotValueAnnotation** :py:mod:`dialoguekit.core.slot_value_annotation`: slot-value pairs, where a slot refers to an entity or a property in the **ontology**.


User preferences
----------------

* Preferences are expressed for specific slot-value pairs, where slots correspond to **entities** or properties in the **ontology**.


Concepts specific to item recommendation scenarios
--------------------------------------------------

* Item: an entity with a unique ID, canonical name, and any number of properties (represented as property-value pairs, where properties correspond to ontology classes).
* ItemCollection: a collection of items.
* Ratings: explicit user preferences on items (normalized into [-1,1]).