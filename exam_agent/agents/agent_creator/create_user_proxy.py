from autogen import UserProxyAgent

def create_user_proxy(name:str = "user_proxy") -> UserProxyAgent:
    proxy = UserProxyAgent(
        name=f"{name}",
        human_input_mode="NEVER",
        is_termination_msg=lambda m: (m.get("content") or "").rstrip().endswith("TERMINATE"),
    )

    return proxy