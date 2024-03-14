import os


def possible_words():

    word_list = os.environ.get("POSSIBLE_WORDS")

    return word_list.splitlines()
