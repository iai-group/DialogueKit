Usage
=====

Simple Example
--------------

This example starts a dialogue in the terminal between a user and an agent that parrots back the user's utterances.


1. Imports

    .. code-block:: python

        from dialoguekit.participant.user import User
        from sample_agents.parrot_agent import ParrotAgent
        from dialoguekit.platforms.terminal_platform import TerminalPlatform
        from dialoguekit.connector.dialogue_connector import DialogueConnector

2. Define agent and user

    .. code-block:: python

        # Participants
        agent = ParrotAgent("A01")
        user = User("U01")

3. Create and connect platform and dialogue connector
    
    .. code-block:: python

        platform = TerminalPlatform()
        dc = DialogueConnector(agent, user, platform)


4. Start conversation

    .. code-block:: python

        dc.start()
        dc.close()
