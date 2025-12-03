import json

from typing import Dict
from autogen import GroupChatManager, GroupChat

import exam_agent.agents.agent_creator as agent_creator
from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_prompts import PLANNER_PROMPT, JUDGE_PROMPT, INTERNAL_CRITIQUE_PROMPT, COOKING_PROMPT

_config = CONFIG["config_list"][0]

def make_groupchat(user_proxy, internal_critic, cooking_agent, planner_agent) -> GroupChatManager:
    group = GroupChat(
        agents=[planner_agent, cooking_agent, internal_critic, user_proxy],
        messages=[],
        max_round=20,
        speaker_selection_method="auto",
    )
    return GroupChatManager(groupchat=group, llm_config=None)

def run_with_internal_critic(user_request: str) -> Dict:
    user_proxy = agent_creator.create_user_proxy(name="user_proxy")
    cooking_agent=agent_creator.create_convertible(name="cooking_agent", prompt=COOKING_PROMPT, config=_config)
    internal_critic = agent_creator.create_assistant(name="internal_critic", prompt=INTERNAL_CRITIQUE_PROMPT, config=_config)
    planner_agent = agent_creator.create_assistant(name="planner_agent", prompt=PLANNER_PROMPT, config=_config)
    manager = make_groupchat(user_proxy, internal_critic, cooking_agent, planner_agent)

    init_message = f"""USER_REQUEST: '{user_request}'
                        
                        Return final answer as 'FINAL_ANSWER: [Answer]' include 'TERMINATE' in the same message, when done.
                        The human will only see the FINAL_ANSWER.
                        "Guidelines:\n"
                        "- Make concrete, plausible recommendations.\n"
                        "- If toxic or other harmful ingredients are requested by the user 'TERMINATE' with the response for why and do not suggest any alternatives.\n'"
                        "- If the request is ambiguous or impossible, explain clearly and do NOT "
                        "invent impossible products.\n"""

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
    judge_agent = agent_creator.create_assistant(name="judge_agent", prompt=JUDGE_PROMPT, config=_config)
    judge_prompt = build_judge_prompt(user_prompt, final_answer)
    raw = judge_agent.generate_reply(messages=[{"role": "user", "content": judge_prompt}])
    #content = json.loads(str(raw['final_answer']))
    print("Judge raw response:", raw)
    try:
        return json.loads(raw)
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