from dialoguekit.agent.agent import Agent, AgentType

class WozAgent(Agent):

    def __init__(self) -> None:
        self._agent_type = AgentType.WOZ