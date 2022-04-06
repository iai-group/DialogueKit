# Rasa parrot

The [Rasa parrot](/dialoguekit/agent/rasa_parrot_agent.py) **Agent** is just an example of how a Rasa agent could be used in DialogueKit.
This **Agent** talks to the [Rasa parrot project](/additional/rasa-parrot/) which does all the processing while the **DialogueKit Rasa Agent** only handles the communication.

## How to use the Rasa parrot

### Start the Rasa service

To use the Rasa parroting **Agent** we firstly need to start the **Rasa service**.

1. Move to the right directory

    ```shell
    cd additional/rasa-parrot
    ```

2. Train the Rasa models

    ```shell
    rasa train
    ```

3. Start the action server

    ```shell
    rasa run actions 
    ```

4. Start service endpoint

    ```shell
    rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
    ```

### Use the Rasa parroting Agent

We can now talk to the Rasa parroting service with the **Agent**.
To do this we need to actually use the **Agent** in our project.
An example can be seen below.

```python
agent = RasaParrotAgent(agent_id="TestId")
user = User("U01")
platform = Platform()
dm = DialogueManager(agent, user, platform)
dm.start()
dm.close()
```

In this example we use a **User** to talk to the Rasa parroting service.
This allows us to interact with the parrot with python inputs.
