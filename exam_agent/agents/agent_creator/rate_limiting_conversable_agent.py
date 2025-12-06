import time

from autogen import ConversableAgent

from exam_agent.tools import Shared_rate_limiter


class Rate_limiter_conversable_agent(ConversableAgent):
    """ConversableAgent subclass that enforces a shared rate limiter."""
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def generate_oai_reply(self,messages,sender,config):
        """
            Wait for the rate limit before calling the base generation method.
        """

        wait_time = Shared_rate_limiter.get_wait_time()

        if wait_time > 0:
            print("Waiting for seconds...".format(wait_time))
            time.sleep(wait_time)

        Shared_rate_limiter.register_call()

        return super().generate_oai_reply(messages,sender,config)