External Agents
===============

DialogueKit is shipped with three agents, which are presented below.
New agents can be implemented by inheriting from :py:class:`dialoguekit.participant.agent.Agent`.

ParrotAgent
-----------

:py:mod:`sample_agents.parrot_agent`

This agent will welcome the user, but will always parrot (echo) what the user says.

MovieBotAgent
-------------

:py:mod:`sample_agents.moviebot_agent`

A connector agent for `IAI MovieBot <https://github.com/iai-group/moviebot>`_ .

WozAgent
--------

:py:mod:`sample_agents.woz_agent`

Allows a real human to play the role of the agent ("wizard") when interacting with a user. This can be useful, e.g., when testing user simulators.