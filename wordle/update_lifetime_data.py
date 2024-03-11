from lifetime_data import lifetime_data
import json


def update_lifetime_data(is_new_player, is_game_over, is_win=False, is_lose=False, is_invalid=False):
    updated_lifetime_data = lifetime_data

    updated_lifetime_data["moves_made"] += 1

    if is_game_over:
        updated_lifetime_data["games_played"] += 1

    if is_new_player:
        updated_lifetime_data["players"] += 1

    if is_win:
        updated_lifetime_data["wins"] += 1

    if is_lose:
        updated_lifetime_data["loses"] += 1

    if is_invalid:
        updated_lifetime_data["invalid_guesses"] += 1

    lifetime_data_file = open("wordle/lifetime_data.py", "w")
    lifetime_data_file.write(f"lifetime_data = {json.dumps(updated_lifetime_data)}")
    lifetime_data_file.close()
