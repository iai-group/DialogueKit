Usage
=============

Simple Example
-------------

1. Define agent and user

.. code-block:: python

    from dialoguekit.core.utterance import Utterance
    from dialoguekit.user.user import User, UserType
    from dialoguekit.agent.parrot_agent import ParrotAgent

    # Participants
    agent = ParrotAgent("A01")
    user = User("U01")

2. Create and connect platform and dialogue manager

.. code-block:: python

    platform = Platform()
    dm = DialogueManager(agent, user, platform)

    user.connect_dialogue_manager(dm)
    agent.connect_dialogue_manager(dm)

3. Start conversation

.. code-block:: python

    dm.start()
    dm.close()
    