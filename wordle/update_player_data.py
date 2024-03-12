from player_data import player_data
from datetime import date
from handle_player_stats import handle_player_stats
import json


def update_player_data(player, guess, is_win, is_valid=True):
    updated_player_data = player_data
    new_player = False

    if player_data.get(player):
        updated_player_data[player]["total_moves"] += 1
        updated_player_data[player]["most_recent_move"] = str(date.today())
        if is_valid:
            if updated_player_data[player]["guess_history"].get(guess):
                updated_player_data[player]["guess_history"][guess] += 1
            else:
                updated_player_data[player]["guess_history"][guess] = 1
        else:
            updated_player_data[player]["total_invalid_guesses"] += 1
    else:
        new_player = True
        updated_player_data[player] = {
            "total_moves": 1,
            "total_winning_moves": 0,
            "total_invalid_guesses": 0,
            "first_move_made": str(date.today()),
            "most_recent_move": str(date.today()),
            "guess_history": {guess: 1},
        }

    if is_win:
        updated_player_data[player]["total_winning_moves"] += 1

    player_data_file = open("wordle/player_data.py", "w")
    player_data_file.write(f"player_data = {json.dumps(updated_player_data)}")
    player_data_file.close()

    handle_player_stats()

    return new_player
