Main concepts
=============

Participant 
-----------
:py:mod:`dialoguekit.participant.participant`

Agents and users are the participants in a dialog. Generally, it is assumed that the agent is a conversational system and the user is a human.
However, the agent might be played by a human ("Wizard-of-Oz") and the human user might be simulated.

DialogueKit assumes the agent to always start the conversation and also end it. (A user can initialize ending a
conversation, but the responsibility lies on the agent to actually stop it.)

Agent
-----
:py:mod:`dialoguekit.agent.agent`

Represents a conversational agent with its own dialogue policy, natural language understanding, and natural language generation components.

DialogueKit is shipped with some sample agents. These are described below:

.. todo:: Move these to a separate sample_agents module outside dialoguekit (https://github.com/iai-group/DialogueKit/issues/153)

* **ParrotAgent**: This agent will welcome the user, but will always parrot (echo) what the user says.

* **RasaParrotAgent**: This agent looks like the **ParrotAgent** to the user, but is actually just a connector to a Rasa conversational agent. This conversational agent is also part of DialogueKit

* **MathAgent**: This agent will ask the user simple arithmetic (addition, subtraction, multiplication and division) questions.

* **MovieBotAgent**: A connector agent for `IAI MovieBot <https://github.com/iai-group/moviebot>`_ .

* **WozAgent**: Allows a real human to play the role of the agent ("wizard") when interacting with a user. This can be useful, e.g., when testing user simulators.

User 
----
:py:mod:`dialoguekit.user.user`

Represents a human interacting with an agent. Has the simplest form of interaction, which are strings to and from the **Dialogue Manager**.


Utterance
---------
:py:mod:`dialoguekit.core.utterance`

An **utterance** by an dialogue participant (agent or user). The utterance holds the participant utterance as clear text. To store additional information such as intent and or annotation the :py:mod:`dialoguekit.core.annotated_utterance` should be used.

Additionally the **annotated_utterance** can store other user defined metadata. **DialogueKit** uses this metadata field for the **Satisfaction Classifier**. The ``metadata`` field is a dictionary with the structure: ``Dict[str, Any]``.

In our case for satisfaction, the ``metadata`` field looks as follows:

.. code-block:: python

    metadata = {
        "satisfaction": int
    }

This metadata will then be used in the natural language generation. You are free to use ``metadata`` for your own use-cases.

Intent 
--------
:py:mod:`dialoguekit.core.intent`

The intent of a participant utterance, i.e., the action which the participant wishes to take by stating the utterance.

As a example we can think of an agents asking the question *"Do you like pizza?"* For this case the intent may be to *INQUIRE* a preference from the user.



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
