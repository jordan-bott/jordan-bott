from player_data import player_data
from datetime import date


def handle_player_stats():
    table_content = """
| Player Name | Total Moves | Total Winning Moves | Total Invalid Guesses | First Move Made | Most Recent Move | Most Guessed Word |
| ----------- | ----------- | ------------------- | --------------------- | --------------- | ---------------- | ------------- |"""
    for item in player_data:
        first_move = date.fromisoformat(player_data[item]["first_move_made"])
        first_move = first_move.strftime("%B %d, %Y")
        recent_move = date.fromisoformat(player_data[item]["most_recent_move"])
        recent_move = recent_move.strftime("%B %d, %Y")
        most_guess = ""
        most_guess_num = 0
        for guess in player_data[item]["guess_history"]:
            if player_data[item]["guess_history"][guess] >= most_guess_num:
                most_guess = guess
                most_guess_num = player_data[item]["guess_history"][guess]
        table_content += f"""
| [{item}](https://github.com/{item}) | {player_data[item]["total_moves"]} | {player_data[item]["total_winning_moves"]} | {player_data[item]["total_invalid_guesses"]} | {first_move} | {recent_move} | {most_guess} ({most_guess_num} times!) |"""

    player_stat_file = open("wordle/stat_sheets/PlayerData.md", "w")
    player_stat_file.write(table_content)
    player_stat_file.close()
