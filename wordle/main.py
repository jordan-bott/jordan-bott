from game_data import game_data
from possible_words import possible_words
from check_word_validity import check_word_validity
from handle_invalid_guess import handle_invalid_guess
from create_schema import create_schema
from update_player_data import update_player_data
from update_lifetime_data import update_lifetime_data
from handle_win import handle_win
from handle_lose import handle_lose
from update_readme import update_readme


import random
import os
import json


def main():

    updated_game_data = game_data

    # check if there is a wordle index
    if game_data["wordle_index"] == "":
        updated_game_data["wordle_index"] = random.randint(0, 2306)

    # pull wordle word based on wordle index
    wordle_word = possible_words()[updated_game_data["wordle_index"]].upper()

    # pull guess from issue meta data
    issue_title = os.environ.get("ISSUE_TITLE")
    guess = issue_title[13:18].upper()

    # pull user from issue meta data
    user = os.environ.get("ISSUE_USER")
    if user not in updated_game_data["players"]:
        updated_game_data["players"].append(user)

    # check if guess is valid
    is_valid = check_word_validity(guess, updated_game_data["guessed_words"])
    if is_valid:
        updated_game_data["guessed_words"].append(guess)
    else:
        is_new_player = update_player_data(user, guess, False, is_valid=False)
        update_lifetime_data(is_new_player, False, guess, wordle_word, is_invalid=True)
        return handle_invalid_guess(user)

    # create schemas
    schema_info = create_schema(wordle_word, guess)
    updated_game_data["schema"] += schema_info[0]
    updated_game_data["letter_schema"] = schema_info[1]

    # update game_data
    updated_game_data["turn_number"] += 1

    game_data_file = open("wordle/game_data.py", "w")
    game_data_file.write(f"game_data = {json.dumps(updated_game_data)}")
    game_data_file.close()

    # check if win & update player meta data
    if wordle_word == guess:
        is_new_player = update_player_data(user, guess, True)
        update_lifetime_data(is_new_player, True, guess, wordle_word, is_win=True)
        return handle_win(wordle_word, user)

    # check if lose & update player meta data
    if updated_game_data["turn_number"] == 6:
        is_new_player = update_player_data(user, guess, False)
        update_lifetime_data(is_new_player, True, guess, wordle_word, is_lose=True)
        return handle_lose(wordle_word, user)

    # update player meta data
    is_new_player = update_player_data(user, guess, False)
    update_lifetime_data(is_new_player, False, guess, wordle_word)

    # update readme
    update_readme(user)


main()
