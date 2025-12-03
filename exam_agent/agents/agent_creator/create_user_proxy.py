from autogen import UserProxyAgent

def create_user_proxy(name:str = "user_proxy") -> UserProxyAgent:
    """
    Creates a user proxy agent
    :param name: name of the proxy
    :return: UserProxyAgent
    """

    proxy = UserProxyAgent(
        name=f"{name}",
        human_input_mode="NEVER",
        is_termination_msg=lambda m: "TERMINATE" in (m.get("content") or ""),
    )

    return proxy