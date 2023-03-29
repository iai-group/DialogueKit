External Agents
===============

DialogueKit is shipped with 4 agents, which are presented below.
New agents can be implemented by inheriting from :py:class:`dialoguekit.participant.agent.Agent`.

ParrotAgent
-----------

:py:mod:`sample_agents.parrot_agent`

This agent will welcome the user, but will always parrot (echo) what the user says.

RasaParrotAgent
---------------

:py:mod:`sample_agents.rasa_parrot_agent`

This agent is just an example of how a Rasa agent could be used in DialogueKit.
It talks to the :py:mod:`external_agents.rasa-parrot` which does all the processing, while the RasaParrotAgent only handles the communication.

How to use the Rasa parrot
""""""""""""""""""""""""""

Start the Rasa service
""""""""""""""""""""""

To use RasaParrotAgent, we firstly need to start the **Rasa service**.

1. Move to the right directory

    .. code-block:: shell

        cd additional/rasa-parrot

2. Train the Rasa models

    .. code-block:: shell

        rasa train

3. Start the action server

    .. code-block:: shell

        rasa run actions 

4. Start service endpoint

    .. code-block:: shell

        rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml


Use RasaParrotAgent
"""""""""""""""""""

We can now talk to the Rasa parroting service with the RasaParrotAgent.
To do this we need to actually use the RasaParrotAgent in our project.
An example can be seen below.

.. code-block:: python

    agent = RasaParrotAgent(agent_id="TestId")
    user = User("U01")
    platform = TerminalPlatform()
    dc = DialogueConnector(agent, user, platform)
    dc.start()
    dc.close()


In this example, we use a user to talk to the Rasa parroting service.
This allows us to interact with the parrot with python inputs.

MovieBotAgent
-------------

:py:mod:`sample_agents.moviebot_agent`

A connector agent for `IAI MovieBot <https://github.com/iai-group/moviebot>`_ .

WozAgent
--------

:py:mod:`sample_agents.woz_agent`

Allows a real human to play the role of the agent ("wizard") when interacting with a user. This can be useful, e.g., when testing user simulators.