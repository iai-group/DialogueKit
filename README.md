# DialogueKit

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

We follow the [IAI Python Style Guide](https://github.com/iai-group/styleguide/tree/master/python).
Documentation can be seen [here.](https://iai-group.github.io/dialoguekit/)

DialogueKit is a library for conversational information access. It contains based classes for fundamental [concepts](docs/concepts.md), such as dialogue participants, dialogue management, [natural language understanding](docs/nlu.md), natural language generation, etc. In addition to the fundamental concepts DialogueKit contains an evaluation module, for evaluating the performance of CIS systems.
Consult the documentation for details.

## Install as a package

**Note:** *Packaging is still a work in progress and may not work perfectly.*

DialogueKit is published to PyPI, install it by running:

```shell
pip install dialoguekit
```

If you want to install a DialogueKit from a specific commit or straight from github this is still possible.

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
      dm.close()
    ```

## Contributors

(Alphabetically ordered by last name) Jafar Afzali, Krisztian Balog, Aleksander Drzewiecki and Shuo Zhang
