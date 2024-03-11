from lifetime_data import lifetime_data


def handle_global_stats():

    most_guessed = ""
    most_guess_num = 0
    for guess in lifetime_data["words_guessed"]:
        if lifetime_data["words_guessed"][guess] >= most_guess_num:
            most_guessed = guess
            most_guess_num = lifetime_data["words_guessed"][guess]

    content = f"""|              |                |
| ---------------- | ----------------------------- |
| Total Moves Made | {lifetime_data["moves_made"]} |
| Total Games Played | {lifetime_data["games_played"]} |
| Total Players Participated | {lifetime_data["players"]} |
| Total Wins | {lifetime_data["wins"]} |
| Total Losses | {lifetime_data["loses"]} |
| Total Invalid Guesses | {lifetime_data["invalid_guesses"]} |
| Most Guessed Word | {most_guessed} ({most_guess_num} times!) |
"""

    global_stat_file = open("wordle/stat_sheets/GlobalData.md", "w")
    global_stat_file.write(content)
    global_stat_file.close()
