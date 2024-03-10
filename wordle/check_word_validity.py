import requests


def check_word_validity(word, guessed_words):
    if len(word) != 5:
        print("Please guess a 5 letter word")
        return False
    if word in guessed_words:
        print("You've already guessed that one!")
        return False
    dict_response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    dict_json = dict_response.json()
    if not isinstance(dict_json, list):
        print("Whoops, that word isn't in the dictionary.")
        return False
    else:
        return True
