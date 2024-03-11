from lifetime_data import lifetime_data
from handle_global_stats import handle_global_stats
import json


def update_lifetime_data(
    is_new_player,
    is_game_over,
    guess,
    wordle_word,
    is_win=False,
    is_lose=False,
    is_invalid=False,
):
    updated_lifetime_data = lifetime_data

    updated_lifetime_data["moves_made"] += 1

    if is_new_player:
        updated_lifetime_data["players"] += 1

    if is_invalid:
        updated_lifetime_data["invalid_guesses"] += 1
    else:
        if updated_lifetime_data["words_guessed"].get(guess):
            updated_lifetime_data["words_guessed"][guess] += 1
        else:
            updated_lifetime_data["words_guessed"][guess] = 1

        if is_game_over:
            updated_lifetime_data["games_played"] += 1

        if is_win:
            updated_lifetime_data["wins"] += 1
            updated_lifetime_data["wordle_words"].append(wordle_word)

        if is_lose:
            updated_lifetime_data["loses"] += 1
            updated_lifetime_data["wordle_words"].append(wordle_word)

    lifetime_data_file = open("wordle/lifetime_data.py", "w")
    lifetime_data_file.write(f"lifetime_data = {json.dumps(updated_lifetime_data)}")
    lifetime_data_file.close()

    handle_global_stats()
