---
orphan: true
---

External Agents
===============

Rasa parrot
--------------

The :py:mod:`sample_agents.rasa_parrot_agent.py` **Agent** is just an example of how a Rasa agent could be used in DialogueKit.
This **Agent** talks to the :py:mod:`additional.rasa-parrot` which does all the processing while the **DialogueKit Rasa Agent** only handles the communication.


How to use the Rasa parrot
^^^^^^^^^^^^^^^^^^^^^^^^^^

Start the Rasa service
""""""""""""""""""""""

To use the Rasa parroting **Agent** we firstly need to start the **Rasa service**.

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


Use the Rasa parroting Agent
""""""""""""""""""""""""""""

We can now talk to the Rasa parroting service with the **Agent**.
To do this we need to actually use the **Agent** in our project.
An example can be seen below.

.. code-block:: python

    agent = RasaParrotAgent(agent_id="TestId")
    user = User("U01")
    platform = Platform()
    dc = DialogueConnector(agent, user, platform)
    dc.start()
    dc.close()


In this example we use a **User** to talk to the Rasa parroting service.
This allows us to interact with the parrot with python inputs.

