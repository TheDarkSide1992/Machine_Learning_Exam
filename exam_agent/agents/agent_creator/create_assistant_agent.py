from autogen import AssistantAgent

from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_prompts import  JUDGE_PROMPT
_config = CONFIG["config_list"][1]



def create_assistant_agent(name:str = "assistant_agent", prompt:str = JUDGE_PROMPT) -> AssistantAgent:
    agent = AssistantAgent(
        name=f"{name}",
        llm_config=_config,
        system_message=prompt,
    )

    return agent