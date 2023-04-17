Usage
=====

Simple Example
--------------

In this example we will have a user that is terminal-based and an agent that
only parrots back what the user said.

1. Imports

    .. code-block:: python

        from dialoguekit.platforms.terminal_platform import TerminalPlatform
        from sample_agents.parrot_agent import ParrotAgent


2. Start conversation

    .. code-block:: python

        platform = TerminalPlatform(ParrotAgent)
        platform.start()
