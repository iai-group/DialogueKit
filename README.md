# DialogueKit

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

We follow the [IAI Python Style Guide](https://github.com/iai-group/styleguide/tree/master/python).

## Install as a package

**Note:** *Packaging is still a work in progress and may not work perfectly.*

As of now DialogueKit is not published as a package, but it is still possible to install it with pip.
The command will install the latest version from the main branch.

* On Windows you may need to run this command before pip installing
  
  ```shell
  ssh -t git github.com    
  ```

* pip install

  ```shell
  pip install git+ssh://git@github.com/iai-group/dialoguekit.git
  ```

If you want to specify a specific commit as the source of the package append the commit hash to the end of the command separated with a "@".

* Specific commit as the source of the package.

  ```shell
  pip install git+ssh://git@github.com/iai-group/dialoguekit.git@faa5c1fca37aaa275105cc1ca7698783719551c2
  ```

## Usage example

**NOTE (TODO):** This usage example will shortly be outdated as of issue [#58.](https://github.com/iai-group/dialoguekit/issues/58)

1. Define agent and user

    ```python
    from dialoguekit.core.utterance import Utterance
    from dialoguekit.user.user import User, UserType
    from dialoguekit.agent.parrot_agent import ParrotAgent

    # Participants
    agent = ParrotAgent("A01")
    user = User("U01")
    ```

2. Create and connect platform and dialogue manager

    ```python
    platform = Platform()
    dm = DialogueManager(agent, user, platform)

    user.connect_dialogue_manager(dm)
    agent.connect_dialogue_manager(dm)
    ```

3. Start conversation

    ```python
      dm.start()

      # Send in user utterance
      dm.register_user_utterance(utterance = Utterance("Hi"))

      dm.close()
    ```

## Contributors

Jafar Afzali, Krisztian Balog, Aleksander Drzewiecki and Shuo Zhang