import json
from statistics import mean
from typing import Dict

from autogen import UserProxyAgent, AssistantAgent, GroupChatManager, GroupChat, ConversableAgent

from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_prompts import JUDGE_PROMPT, INTERNAL_CRITIQUE_PROMPT, COOKING_PROMPT, PLANNER_PROMPT
_config = CONFIG["config_list"][0]

def create_cooking_agent(name:str = "cooking_agent", prompt:str = COOKING_PROMPT) -> ConversableAgent:
    agent =  ConversableAgent(
        name=f"{name}",
        llm_config=_config,
        system_message=prompt,

    )

    return agent

def create_internal_critic_agent(name:str = "internal_critic", prompt:str = INTERNAL_CRITIQUE_PROMPT) -> AssistantAgent:
    agent =  AssistantAgent(
        name=f"{name}",
        llm_config=_config,
        system_message=prompt,
    )

    return agent

def create_judge_agent(name:str = "judge_agent", prompt:str = JUDGE_PROMPT) -> AssistantAgent:
    agent = AssistantAgent(
        name=f"{name}",
        llm_config=_config,
        system_message=prompt,
    )

    return agent

def create_planner_agent(name:str = "planner_agent", prompt:str = PLANNER_PROMPT) -> AssistantAgent:
    planner = AssistantAgent(
        name=f"{name}",
        llm_config=_config,
        system_message=prompt,
    )
    return planner

def create_user_proxy(name:str = "user_proxy") -> UserProxyAgent:
    agent = UserProxyAgent(
        name=f"{name}",
        human_input_mode="NEVER",
        is_termination_msg=lambda m: (m.get("content") or "").rstrip().endswith("TERMINATE"),
    )

    return agent

def make_groupchat(planner_agent, user_proxy, internal_critic, cooking_agent) -> GroupChatManager:
    group = GroupChat(
        agents=[planner_agent, cooking_agent, internal_critic, user_proxy],
        messages=[],
        max_round=30,
        speaker_selection_method="auto",
    )
    return GroupChatManager(groupchat=group)

def run_with_internal_critic(user_request: str) -> Dict:
    planner_agent = create_planner_agent()
    user_proxy = create_user_proxy()
    cooking_agent = create_cooking_agent()
    internal_critic = create_internal_critic_agent()
    manager = make_groupchat(planner_agent, user_proxy, internal_critic, cooking_agent)


    init_message = f"""USER_REQUEST: '{user_request}'
                        Workflow for agents:
                        planner_agent: Produce a concise numbered plan for which agents need to do what.
                        cooking_agent: Needs to find healthy recipies based on the USER_REQUEST.
                        cooking_agent: If the request is ambiguous or impossible, explain clearly and do NOT "
                        "invent impossible or dangerous recipies.."
                        cooking_agent: Using the plan, read USER_REQUEST and propose an answer as 'DRAFT: ...'.
                        internal_critic: On a DRAFT, respond with 'OK:' or 'CRITIQUE:'.
                        cooking_agent: if you get CRITIQUE, revise and send a new 'DRAFT:'.
                        When internal_critic is satisfied, cooking_agent sends 
                        'FINAL_ANSWER: ...' and also includes 'TERMINATE' in the same message.
                        
                        Return final answer as 'FINAL_ANSWER: [Answer]' include 'TERMINATE' in the same message, when done.
                        The human will only see the FINAL_ANSWER."""

    final = user_proxy.initiate_chat(
        manager,
        message=init_message,
    )

    trace = list(manager.groupchat.messages)

    final_answer = None
    for msg in reversed(trace):
        if msg.get("name") == "cooking_agent" and isinstance(msg.get("content"), str):
            content = msg["content"]
            if "FINAL_ANSWER:" in content:
                final_answer = content
                break

    return {
        "final_answer": final_answer or str(final),
        "trace": trace,
    }

def build_judge_prompt(user_prompt: str, final_answer: str) -> str:
    return (
        f"""You are evaluating a recipe answer.\n
        User prompt:\n"
        \"\"\"{user_prompt}\"\"\"\n"
        Final answer from the agent (after internal critic and GroupChat):\n
        "\"\"\"{final_answer}\"\"\""""
    )

def llm_judge_score(user_prompt: str, final_answer: str) -> Dict:
    print("final answer:", final_answer)
    judge_agent = create_judge_agent()
    judge_prompt = build_judge_prompt(user_prompt, final_answer)
    raw = judge_agent.generate_reply(messages=[{"role": "user", "content": judge_prompt}])
    content = json.loads(str(raw['content']))
    print("Judge raw response:", content)
    try:
        return content
    except json.JSONDecodeError:
        return {
            "final_answer": final_answer,
            "rationale": "Judge JSON parse failed.",
            "completeness": 0.0,
            "quality": 0.0,
            "healthiness": 0.0,
            "transparency": 0.0,
            "total": 0.0,
        }

def evaluate_prompt(prompt: str) -> Dict:
    # 1) Run through GroupChat with internal critic
    internal = run_with_internal_critic(prompt)
    final_answer = internal["final_answer"]

    # 2) External judge scores the final answer
    judge_scores = llm_judge_score(prompt, final_answer)

    return {
        "prompt": prompt,
        "final_answer": final_answer,
        "judge_scores": judge_scores,
    }


def start_agent(prompt:str=""):
    if prompt.strip() == "":
        raise ValueError("Invalid prompt.")

    result = evaluate_prompt(prompt=prompt)

    print(f"agents agreed on the following answer: \n{result['final_answer']}")