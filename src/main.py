import os
import random
from typing import List

import markovify
import pandas as pd


def format_real_headlines(df: pd.DataFrame) -> List[str]:
    assert "title" in df

    headlines = df["title"].tolist()
    for i in range(len(headlines)):
        headlines[i] = headlines[i].title()

    return headlines


def print_intro():
    print("Welcome to the Florida Man game!")
    print("The game is simple. We'll provide you with a headline, and it's")
    print("your job to determine whether the headline is REAL or FAKE!")


def input_choices(input_str: str, choices: List[str]) -> str:
    """
    Requires user to input valid options.

    Args:
        input_str: The string to display in the "input" function call.
        options: The allowed options to compare against.
    Returns:
        One of the options in options.
    """

    user_input = input(input_str)
    while not user_input in choices:
        print("Sorry, that's not a recognized input.")
        user_input = input(input_str)
    return user_input


def main():
    real_headlines_df = pd.read_csv("data/real_reddit_posts.csv")
    real_headlines = format_real_headlines(real_headlines_df)
    model = markovify.NewlineText("\n".join(real_headlines))

    print_intro()

    print("To exit the game, please enter 'quit' at any time.")

    choices = ["real", "fake", "quit"]
    choice_str = ", ".join(choices)
    prompt_str = f"Please enter one of the following options: [{choice_str}]\n"

    user_input = None

    while user_input != "quit":
        real = random.choice(real_headlines)
        fake = model.make_sentence(max_overlap_ratio=0.6, tries=100_000)

        possible_headlines = [real, fake]

        displayed = random.choice(possible_headlines)

        print("Is the following headline real or fake?")
        print("\n")
        print(displayed)
        print("\n")
        choice = input_choices(prompt_str, choices)
        os.system('clear')

        if choice == "quit":
            break
        elif choice == "real" and displayed == real:
            print("Correct! It was a real headline.")
        elif choice == "fake" and displayed == fake:
            print("Correct! It was a fake headline.")
        else:
            actual_type = "real" if displayed == "real" else 'fake'
            print(f"Sorry, the headline was actually {actual_type}")

if __name__ == "__main__":
    main()
