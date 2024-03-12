import requests
import os


def check_word_validity(word, guessed_words):
    if len(word) != 5:
        print("Please guess a 5 letter word")
        return False
    if word in guessed_words:
        print("You've already guessed that one!")
        return False
    print(list(os.environ.get("DISALLOWED_WORDS")))
    if word in os.environ.get("DISALLOWED_WORDS"):
        print(
            "Hmm that word isn't allowed. Please be respectful/appropriate with your guess."
        )
        return False
    dict_response = requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    )
    if dict_response is not None:
        dict_json = dict_response.json()
    else:
        print("Bad API response")
        return False
    if not isinstance(dict_json, list):
        print("Whoops, that word isn't in the dictionary.")
        return False
    else:
        return True
