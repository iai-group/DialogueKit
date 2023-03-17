Participant 
===========

:py:mod:`dialoguekit.participant.participant`

Agents and users are the participants in a dialogue. Generally, it is assumed that the agent is a conversational system and the user is a human.
However, the agent might be played by a human ("Wizard-of-Oz") and the human user might be simulated.

DialogueKit assumes the agent to always start the conversation and also end it. (A user can initialize ending a conversation, but the responsibility lies on the agent to actually stop it.)

Agent
-----

:py:mod:`dialoguekit.participant.agent`

Represents a conversational agent with some intelligent capabilities (typically defined by the dialogue policy, natural language understanding, and natural language generation components).

DialogueKit is shipped with some sample agents (see :doc:`external_agents` for more details).

User 
----

:py:mod:`dialoguekit.participant.user`

Represents a human interacting with an agent in natural language text.

User preferences
^^^^^^^^^^^^^^^^

:py:mod:`dialoguekit.participant.user_preferences`

User's preferences are expressed for specific slot-value pairs, where slots correspond to entities or properties in the domain.
