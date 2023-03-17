Dialogue Orchestration
======================

DialogueKit use a connector to orchestrate the dialogue between the participants (i.e., agent and user).
This connector is linked to a platform that facilitate the communication between the participants.

Dialogue Connector 
------------------

:py:mod:`dialoguekit.connector.dialogue_connector`

Holds and orchestrates the conversation between the participants.

Platform 
--------

:py:mod:`dialoguekit.platforms.platform`

The platform's responsibility is to facilitate the conversation and ensure that the participant can see the agent's utterances and reply to it.
DialogueKit includes a simple terminal-based platform. However, it can support other platforms by facilitating communication via POST requests. 
