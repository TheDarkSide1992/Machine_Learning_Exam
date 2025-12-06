from autogen import AssistantAgent

from exam_agent.agents.agent_creator.rate_limiting_assistant_agent import Rate_limiter_assistant_agent
from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_system_prompts import  JUDGE_SYSTEM_MESSAGE as _assistant_fallback
_config = CONFIG["config_list"][0]



def create_assistant_agent(name:str = "assistant_agent", message:str = _assistant_fallback, config: dict[str, str | float | int | bool | None] | dict[str, str] | dict[str, str | float | bool | int | None | dict[str, int | float]] = _config) -> AssistantAgent:
    """
    Creates an assistant agent
    :param name: Name of the assistant
    :param message: agent system message, fallback to JUDGE_SYSTEM_MESSAGE, Unreliable depending on agent use
    :param config: agent configuration
    :return: AssistantAgent
    """

    agent = Rate_limiter_assistant_agent(
        name=f"{name}",
        llm_config=config,
        system_message=message,
    )

    return agent