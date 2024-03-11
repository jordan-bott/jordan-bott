from player_data import player_data
from datetime import datetime
import json


def update_player_data(player, guess, is_win):
    updated_player_data = player_data
    new_player = False

    if player_data.get(player):
        updated_player_data[player]["total_moves"] += 1
        updated_player_data[player]["most_recent_move"] += str(datetime.now())
        updated_player_data[player]["guess_history"].append(guess)
    else:
        new_player = True
        updated_player_data[player] = {
            "total_moves": 1,
            "total_winning_moves": 0,
            "first_move_made": str(datetime.now()),
            "most_recent_move": str(datetime.now()),
            "guess_history": [guess]
        }

    if is_win:
        updated_player_data["total_winning_moves"] += 1

    player_data_file = open("wordle/player_data.py", "w")
    player_data_file.write(f"player_data = {json.dumps(updated_player_data)}")
    player_data_file.close()

    return new_player
