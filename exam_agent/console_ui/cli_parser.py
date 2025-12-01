import argparse


def get_parser_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("-P", "--prompt", type=str, help=f"Allows you to enter your prompt, before application start.")
    parser.add_argument("-G", "--generate-recipe", action="store_true",
                        help="Allows the agent to generate its own recipe. If flag is false the ai wil search for a recipe instead. this flag is of by default.")
    parser.add_argument("-C", "--continuous-chat", action="store_true",
                        help="Allows you to continuously prompt the agent without th application classing flag is true")
    args = parser.parse_args()

    return args