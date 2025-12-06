from autogen import ConversableAgent

from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_system_prompts import  COOKING_SYSTEM_MESSAGE as _convirsible_fallback
_config = CONFIG["config_list"][1]



def create_convertible_agent(name:str = "create_convertible_agent", message:str = _convirsible_fallback, config: dict[str, str | float | int | bool | None] | dict[str, str] | dict[str, str | float | bool | int | None | dict[str, int | float]] = _config) -> ConversableAgent:
    """
        Creates an conversible agent
        :param name: Name of the assistant
        :param message: agent prompt, fallback to COOKING_PROMPT, Unreliable depending on agent use
        :param config: agent configuration
        :return: ConversableAgent
        """
    agent =  ConversableAgent(
        name=f"{name}",
        llm_config=config,
        system_message=message,

    )

    return agent