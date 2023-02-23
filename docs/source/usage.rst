Usage
=====

Simple Example
--------------

In this example we will have a user that is terminal-based and an agent that
only parrots back what the user said.

1. Imports

    .. code-block:: python

        from dialoguekit.participant.user import User
        from sample_agents.parrot_agent import ParrotAgent
        from dialoguekit.platforms.platform_terminal import TerminalPlatform
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

        user.connect_dialogue_connector(dc)
        agent.connect_dialogue_connector(dc)


4. Start conversation

    .. code-block:: python

        dc.start()
        dc.close()
