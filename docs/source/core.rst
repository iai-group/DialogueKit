Core components
===============

This page presents the core components of DialogueKit to represent a dialogue and its elements. 

Utterance
---------

:py:mod:`dialoguekit.core.utterance`

Dialogue participants exchange utterances, which are represented as raw text. 

AnnotatedUtterance
^^^^^^^^^^^^^^^^^^

:py:mod:`dialoguekit.core.annotated_utterance`

This class enrich Utterance with an intent, annotations, and/or freely definable metadata.

Intent 
------

:py:mod:`dialoguekit.core.intent`

The intent represents the action expressed by a participant in an utterance. For example, an agent asking the question *"Do you like pizza?"* may have the intent to *INQUIRE* a preference from the user.

Domain 
------

:py:mod:`dialoguekit.core.domain`

Defines the types of entities and the set of properties ("slots") for each entity type.

Annotations
-----------

:py:mod:`dialoguekit.core.annotation`

By default an annotation has a slot and a value, for example the slot *price* has the value *$10* in the following utterance *"This dish costs $10."*.

DialogueKit is shipped with:

* **SlotValueAnnotation** :py:mod:`dialoguekit.core.slot_value_annotation`: slot-value pairs, where a slot refers to an entity or a property in the domain.

Other types of annotation can be implemented by inheriting from :py:class:`dialoguekit.core.annotation.Annotation`.

Dialogue
--------

:py:mod:`dialoguekit.core.dialogue`

This object contains all the information related to the dialogue such as the utterances, the identity of participants, and other metadata.
