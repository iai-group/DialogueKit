Natural Language Understanding (NLU)
====================================

The NLU component is responsible for obtaining a structured representation of text utterances. Currently, it entails dialogue acts recognition, key-value annotation (e.g., user sentiment), and user satisfaction prediction.

Dialogue Acts Recognition
-------------------------

A dialogue act is a semantic unit that comprises a single intent and slot-value pairs; an utterance can have multiple dialogue acts. The task of dialogue act recognition can be seen as a combination of intent classification and slot filling. These subtasks can be performed jointly or disjointly. DialogueKit is designed to support both approaches, see base classes: :py:mod:`dialoguekit.nlu.dialogue_acts_extractor.DialogueActsExtractor` and :py:mod:`dialoguekit.nlu.disjoint_dialogue_act_extractor.DisjointDialogueActExtractor`.

Disjoint Dialogue Act Recognition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this component, the task of intent classification and slot filling are performed in a disjoint manner. That is, the intent classifier predicts the intent of the utterance, while the slot filler predicts the slot-value pairs in the utterance. These are then combined to form one dialogue act.

Intent Classification
"""""""""""""""""""""

There is a simple Cosine intent classifier implemented in DialogueKit, which can be used out-of-the-box :py:mod:`dialoguekit.nlu.models.intent_classifier_cosine`

Slot Filling
""""""""""""

There are no slot filling models implemented in the current version of DialogueKit. However, the base class :py:mod:`dialoguekit.nlu.models.slot_filler.SlotFiller` can be extended to implement a slot filling model.

User Satisfaction Prediction
----------------------------

User satisfaction prediction entails the task of predicting a user's satisfaction with the system, based on the conversation.
We model this as a classification task, where, given the previous *n* user-agent turns, the task of the classifier is to predict the user satisfaction on a scale from 1-5:

#. Very dissatisfied
#. Dissatisfied
#. Normal
#. Satisfied
#. Very satisfied

The current satisfaction classifier is a SVM model pre-trained on `english data <https://github.com/sunnweiwei/user-satisfaction-simulation>`_.