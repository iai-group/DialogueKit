Usage
=====

Simple Example
--------------

This example starts a dialogue in the terminal between a user and an agent that parrots back the user's utterances.


1. Imports

    .. code-block:: python

        from dialoguekit.platforms.terminal_platform import TerminalPlatform
        from sample_agents.parrot_agent import ParrotAgent


2. Start conversation

    .. code-block:: python

        platform = TerminalPlatform(ParrotAgent)
        platform.start()
