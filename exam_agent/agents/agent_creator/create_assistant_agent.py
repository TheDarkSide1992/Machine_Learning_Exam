from autogen import AssistantAgent

from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_prompts import  JUDGE_PROMPT as _assistant_fallback
_config = CONFIG["config_list"][1]



def create_assistant_agent(name:str = "assistant_agent", prompt:str = _assistant_fallback, config: dict[str, str | float | int | bool | None] | dict[str, str] | dict[str, str | float | bool | int | None | dict[str, int | float]] = _config) -> AssistantAgent:
    """
    Creates an assistant agent
    :param name: Name of the assistant
    :param prompt: agent prompt, fallback to JUDGE_PROMPT, Unreliable depending on agent use
    :param config: agent configuration
    :return: AssistantAgent
    """

    agent = AssistantAgent(
        name=f"{name}",
        llm_config=config,
        system_message=prompt,
    )

    return agent