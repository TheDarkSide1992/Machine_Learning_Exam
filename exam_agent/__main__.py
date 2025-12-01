import argparse
from exam_agent.agents import start


def main(prompt:str=None, continuous_chat:bool=False, generate_recipe:bool=False):
    print("Starting up.....")

    while continuous_chat:
        prompt = get_user_input()
        start(prompt=prompt)


def get_user_input() -> str:
    prompt = input("Please enter your prompt: ")

    while prompt.strip() == "":
        prompt = input("Invalid input, please enter your prompt: ")

    return prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-P", "--prompt", type=str, help=f"Allows you to enter your prompt, before application start.")
    parser.add_argument("-G", "--generate-recipe", action="store_true",
                        help="Allows the agent to generate its own recipe. If flag is false the ai wil search for a recipe instead. this flag is of by default.")
    parser.add_argument("-C", "--continuous-chat", action="store_true",
                        help="Allows you to continuously prompt the agent without th application classing flag is true")
    args = parser.parse_args()

    prompt = None;
    cc = False;
    gr = False


    if args.prompt is not None:
        prompt = args.prompt
    if args.generate_recipe:
        gr = args.generate_recipe
    if args.continuous_chat:
        cc = args.continuous_chat

    main(prompt=prompt, continuous_chat=cc, generate_recipe=gr)