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
    - Intent: represents the dialogue action.
    - SlotValueAnnotation: slot-value pairs, where a slot refers to an entity or a property in the ontology.
  * User preferences: preferences are expressed for specific slot-value pairs, where slots correspond to entities or properties in the ontology.

### Concepts specific to item recommendation scenarios

  * Item: an entity with a unique ID, canonical name, and any number of properties (represented as property-value pairs, where properties correspond to ontology classes).
  * ItemCollection: a collection of items.
  * Ratings: explicit user preferences on items (normalized into [-1,1]).


## Contributors

Krisztian Balog, Shuo Zhang
