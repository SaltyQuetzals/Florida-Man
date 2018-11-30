import os
import random
import re
from typing import List, Tuple

import markovify
import nltk
import pandas as pd

MAX_OVERLAP = 0.4
MIN_CHARS = 30
MAX_CHARS = 100


def format_real_headlines(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    assert "title" in df
    assert "url" in df

    headlines_and_urls = df[["title", "url"]].values.tolist()
    formatted_headlines = []
    urls = []
    for headline, url in headlines_and_urls:
        headline = headline.replace("&amp;", "&")
        headline = headline.replace("Floridaman", "Florida man")
        headline = headline.title()
        formatted_headlines.append(headline)
        urls.append(url)
    return formatted_headlines, urls


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
    print("Loading headline data...", end="")
    real_headlines_df = pd.read_csv("data/real_reddit_posts.csv")
    real_headlines, real_urls = format_real_headlines(real_headlines_df)
    print("done.")
    print("Training model...", end="")
    model = markovify.NewlineText("\n".join(real_headlines), state_size=1)
    print("done.")

    os.system("clear")
    print_intro()

    print("To exit the game, please enter 'quit' at any time.")

    choices = ["real", "fake", "quit"]
    choice_str = ", ".join(choices)
    prompt_str = f"Please enter one of the following options: [{choice_str}]\n"

    user_input = None

    while user_input != "quit":
        r_line, r_url = random.choice(list(zip(real_headlines, real_urls)))
        f_line = model.make_short_sentence(
            MAX_CHARS, min_chars=MIN_CHARS, max_overlap_ratio=MAX_OVERLAP
        )
        while f_line is None:
            f_line = model.make_short_sentence(
                MAX_CHARS, min_chars=MIN_CHARS, max_overlap_ratio=MAX_OVERLAP
            )
        print("Is the following headline REAL or FAKE?\n\n")

        displayed_line = random.choice([r_line, f_line])
        print(displayed_line, end="\n\n")
        user_input = input_choices(prompt_str, choices)
        os.system("clear")

        if user_input == "quit":
            break
        elif user_input == "real" and displayed_line == r_line:
            print(f"Correct! The headline was real. Check it out here: {r_url}")
        elif user_input == "fake" and displayed_line == f_line:
            print("Correct! The headline was fake.")
        else:
            actual_type = "real" if displayed_line == r_line else "fake"
            print(f"Incorrect! The headline was actually {actual_type}")
            if actual_type == "real":
                print(f"Don't believe me? Check it out here: {r_url}")


if __name__ == "__main__":
    main()
