from autogen import ConversableAgent

from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_prompts import  COOKING_PROMPT as _convirsible_fallback
_config = CONFIG["config_list"][1]



def create_convertible_agent(name:str = "create_convertible_agent", prompt:str = _convirsible_fallback) -> ConversableAgent:
    """
        Creates an conversible agent
        :param name: Name of the assistant
        :param prompt: agent prompt, fallback to COOKING_PROMPT, Unreliable depending on agent use
        :return: ConversableAgent
        """
    agent =  ConversableAgent(
        name=f"{name}",
        llm_config=_config,
        system_message=prompt,

    )

    return agent