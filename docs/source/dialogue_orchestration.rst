Dialogue Orchestration
======================

DialogueKit uses a connector to orchestrate the dialogue between the participants (i.e., agent and user).
This connector is linked to a platform that facilitates the communication between the participants.

Dialogue Connector 
------------------

:py:mod:`dialoguekit.connector.dialogue_connector`

Holds and orchestrates the conversation between the participants.

Platform 
--------

:py:mod:`dialoguekit.platforms.platform`

The platform's responsibility is to facilitate the conversation and ensure that the participant can see the agent's utterances and reply to it.
DialogueKit includes a simple terminal-based platform.
However, other platforms (e.g., various messaging apps/services, such as Telegram or Facebook Messenger or Flask chat) can be created by inheriting from :py:class:`dialoguekit.platforms.platform.Platform`.
