# Usage

## Simple Example

In this example we will have a user that is terminal-based and an agent that
only parrots back what the user said.

1. Imports

    ```python
    from dialoguekit.user.user import User
    from dialoguekit.agent.parrot_agent import ParrotAgent
    from dialoguekit.platforms.platform import Platform
    from dialoguekit.manager.dialogue_manager import DialogueManager
    ```

2. Define agent and user

   ```python
    # Participants
    agent = ParrotAgent("A01")
    user = User("U01")
    ```

3. Create and connect platform and dialogue manager

   ```python
    platform = Platform()
    dm = DialogueManager(agent, user, platform)

    user.connect_dialogue_manager(dm)
    agent.connect_dialogue_manager(dm)
    ```

4. Start conversation

   ```python
    dm.start()
    dm.close()
    ```
