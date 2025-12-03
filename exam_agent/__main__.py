from exam_agent.console_ui import COLLORS, get_args
from exam_agent.agents import start

def main(prompt:str=None, continuous_chat:bool=False, generate_recipe:bool=False, defaults_prompts:bool=False):
    print("Starting up.....")

    if defaults_prompts:
        #TODO Use default already written prompts
        return

    if(prompt == None  and continuous_chat==False):
        print(f"{COLLORS.WARNING} You need to select a type of input.")
        print(f"{COLLORS.DEFUALT} using default")
        start("make me a recipe for a sandwich") #TODO Change the to a list of existing prompts


    if(prompt != None):
        start(prompt)
        print("Type the recipe you would like to start")

    while continuous_chat:
        prompt = get_user_input()
        print("Type the recipe you would like to start")

        start(prompt=prompt)


def get_user_input() -> str:
    prompt = input("Please enter your prompt: ")

    while prompt.strip() == "":
        prompt = input(f"{COLLORS.WARNING}Invalid input, please enter your prompt: ")

    print(f"{COLLORS.OK} prompt:    {prompt}{COLLORS.DEFUALT}")

    return prompt

if __name__ == "__main__":
    args = get_args()

    prompt = None
    cc = False
    gr = False
    dp = False

    if args.prompt is not None:
        prompt = args.prompt
    if args.generate_recipe:
        gr = args.generate_recipe
    if args.continuous_chat:
        cc = args.continuous_chat
    if args.defaults_prompts:
        dp = args.defaults_prompts

    main(prompt=prompt, continuous_chat=cc, generate_recipe=gr, defaults_prompts=dp)