# DialogueKit

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/adrzewiecki/35bb996459f0949b38da651c66cf95cb/raw/coverage.dialoguekit.main.json) [![PyPi version](https://img.shields.io/pypi/v/dialoguekit)](https://pypi.org/project/dialoguekit/)

DialogueKit is a library for conversational information access (CIA). It contains based classes for fundamental [concepts](docs/concepts.md), such as dialogue participants, dialogue management, [natural language understanding](docs/nlu.md), natural language generation, etc. In addition to the fundamental concepts DialogueKit contains an evaluation module, for evaluating the performance of and CIA systems.
Consult the [documentation](https://iai-group.github.io/DialogueKit/) for details.

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

## Planned future features

  * [Rework imports](https://github.com/iai-group/dialoguekit/issues/123)
  * [Versioning for docs](https://github.com/iai-group/dialoguekit/issues/124)
  * [Unified dialogue reader](https://github.com/iai-group/dialoguekit/issues/140)

## Conventions

We follow the [IAI Python Style Guide](https://github.com/iai-group/styleguide/tree/master/python).

## Contributors

(Alphabetically ordered by last name) Jafar Afzali, Krisztian Balog, Aleksander Drzewiecki and Shuo Zhang
