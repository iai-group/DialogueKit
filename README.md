# DialogueKit

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![PyPi version](https://img.shields.io/pypi/v/dialoguekit)](https://pypi.org/project/dialoguekit/) 
![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/adrzewiecki/35bb996459f0949b38da651c66cf95cb/raw/coverage.DialogueKit.main.json) 
![Tests](https://img.shields.io/github/actions/workflow/status/iai-group/DialogueKit/merge.yaml?label=Tests&branch=main)
![Python version](https://img.shields.io/badge/python-3.9-blue)

DialogueKit is a library for conversational information access (CIA). It contains based classes for fundamental [concepts](https://iai-group.github.io/DialogueKit/main/concepts.html), such as dialogue participants, dialogue management, [natural language understanding](https://iai-group.github.io/DialogueKit/main/nlu.html), natural language generation, etc. In addition to the fundamental concepts DialogueKit contains an evaluation module, for evaluating the performance of and CIA systems.
Consult the [documentation](https://iai-group.github.io/DialogueKit/main/) for details.

## Install as a package

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
    from dialoguekit.participant.user import User, UserType
    from sample_agents.parrot_agent import ParrotAgent

    # Participants
    agent = ParrotAgent("A01")
    user = User("U01")
    ```

2. Create and connect platform and dialogue manager

    ```python
    from dialoguekit.platforms.platform import Platform
    from dialoguekit.manager.dialogue_manager import DialogueManager

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

## Conventions

We follow the [IAI Python Style Guide](https://github.com/iai-group/styleguide/tree/main/python).

## Contributors

(Alphabetically ordered by last name) 

  * Jafar Afzali (2022)
  * Krisztian Balog (2021-present)
  * Nolwenn Bernard (2022-present)
  * Aleksander Drzewiecki (2022)
  * Shuo Zhang (2021)
