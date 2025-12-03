import json

from pprint import pprint
from typing import Dict
from autogen import GroupChatManager, GroupChat

import exam_agent.agents.agent_creator as agent_creator
from exam_agent.config import LLM_CONFIG as CONFIG
from exam_agent.agents.agent_prompts import PLANNER_PROMPT, JUDGE_PROMPT, INTERNAL_CRITIQUE_PROMPT, COOKING_PROMPT
from exam_agent.tools import db_search

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

    cooking_agent.register_for_llm(name="search_tool", description="a tool that can take a ingredient and look it up in a openFoodTox database, to check if its toxic")(db_search)
    user_proxy.register_for_execution(name="search_tool")(db_search)

    init_message = f"""USER_REQUEST: '{user_request}'
                        Workflow for agents:
                        planner_agent: Break down the USER_REQUEST into subtasks for other agents.
                        cooking_agent: Needs to find healthy recipies based on the USER_REQUEST.
                        cooking_agent: If the request is ambiguous or impossible, explain clearly and do NOT "
                        "invent impossible or dangerous recipies.."
                        cooking_agent: read USER_REQUEST and propose an answer as 'DRAFT: ...'.
                        internal_critic: when you see a DRAFT, respond with 'OK:' or 'CRITIQUE:'.
                        cooking_agent: if you get CRITIQUE, revise and send a new 'DRAFT:'.
                        When internal_critic responds with 'OK:' it should include 'TERMINATE' in the same message.
                        When internal_critic responds with 'OK:' and 'TERMINATE' internal_critic should immediately after return final answer as 'FINAL_ANSWER: [Answer]' include 'TERMINATE' in the same message, when done.
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
    judge_agent = agent_creator.create_assistant(name="judge_agent", prompt=JUDGE_PROMPT, config=_config)
    judge_prompt = build_judge_prompt(user_prompt, final_answer)
    raw = judge_agent.generate_reply(messages=[{"role": "user", "content": judge_prompt}])
    try:
        return raw.get("content")
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

    print("\n--- Prompt ---\n")
    print(result["prompt"])

    print("\n--- Final Answer ---\n")
    print(result["final_answer"].encode().decode("unicode_escape"))

    print("\n--- Scores ---\n")
    pprint(result["judge_scores"], indent=4)