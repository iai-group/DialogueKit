Dialogue Representation
=======================

This page presents the core components of DialogueKit to represent a dialogue and its elements. 

Utterance
---------

:py:mod:`dialoguekit.core.utterance`

Dialogue participants exchange utterances, which are represented as raw text. 

AnnotatedUtterance
^^^^^^^^^^^^^^^^^^

:py:mod:`dialoguekit.core.annotated_utterance`

This class enriches Utterance with an intent, annotations, and/or freely definable metadata.

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

By default, an annotation has a key and an optional value, for example, the key *satisfaction* has the value *True* in the following utterance *"That's perfect, thanks!"*.

DialogueKit is shipped with:

* **SlotValueAnnotation** :py:mod:`dialoguekit.core.slot_value_annotation`: slot-value pairs, where a slot refers to an entity or a property in the domain.

Other types of annotation can be implemented by inheriting from :py:class:`dialoguekit.core.annotation.Annotation`.

Feedback
--------

:py:mod:`dialoguekit.core.feedback`

This object represents user's feedback. Currently only binary feedback (like/dislike) is supported on the utterance level. Later, it might be extended to graded feedback as well as conversation-level feedback.

Dialogue
--------

:py:mod:`dialoguekit.core.dialogue`

This object contains all the information related to the dialogue, such as the utterances, the identity of participants, and other metadata.
