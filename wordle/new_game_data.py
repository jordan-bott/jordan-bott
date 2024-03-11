from new_letter_schema import new_letter_schmea
import json


def new_game_data():
    game_data = {
        "wordle_index": "",
        "turn_number": 0,
        "guessed_words": [],
        "players": [],
        "schema": "",
        "letter_schema": "".join(new_letter_schmea),
    }

    game_data_file = open("wordle/game_data.py", "w")
    game_data_file.write(f"game_data = {json.dumps(game_data)}")
    game_data_file.close()
