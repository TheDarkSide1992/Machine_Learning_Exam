import argparse


def get_parser_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("-P", "--prompt", type=str, help=f"Allows you to enter your prompt, before application start.")
    parser.add_argument("-C", "--continuous-chat", action="store_true",
                        help="Allows you to continuously prompt the agent without the application closing, flag is true by default")
    args = parser.parse_args()

    return args