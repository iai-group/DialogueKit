# Main concepts

* **Participant**
  * Represents a participant in the conversation.
  * **User** and **Agent** are Participants
* **Agent**
  * Represents a bot, with its own set of logic, **NLU** and **NLG**.
* **User**
  * Represents a human interacting. Has the simplest form of interaction, which are strings to and from the **Dialogue Manager**.
* **Utterance**
  * An **utterance** by an **Agent** or **User**. The utterance holds the participant utterance as clear text and can hold additionally to the intent and or annotation.
* **Platform**
  * The platform is the way the **Participants** communicate with each other. This can be native to DialogueKit or other forms as REST APIs or other methods.
* **Dialogue Manager**
  * Holds and orchestrates the conversation between the participants.
* **Ontology**
  * Defines the types of entities and the set of properties ("slots") for each entity type.
* There are two types of annotations
  * **Intent**: represents the dialogue action.
  * **SlotValueAnnotation**: slot-value pairs, where a slot refers to an entity or a property in the **ontology**.
* **User preferences**
  * Preferences are expressed for specific slot-value pairs, where slots correspond to **entities** or properties in the **ontology**.

## Concepts specific to item recommendation scenarios

* Item: an entity with a unique ID, canonical name, and any number of properties (represented as property-value pairs, where properties correspond to ontology classes).
* ItemCollection: a collection of items.
* Ratings: explicit user preferences on items (normalized into [-1,1]).