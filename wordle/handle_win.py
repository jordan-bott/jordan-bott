from game_data import game_data
from new_game_data import new_game_data
from lifetime_data import lifetime_data
import json


def handle_win(wordle_word, user):

    shield_user = ""
    for letter in user:
        if letter == "-":
            shield_user += "--"
        elif letter == "_":
            shield_user += "__"
        else:
            shield_user += letter

    letter_schema = "".join(game_data["letter_schema"])

    readme_content = f"""
Hi! 👋🏼 I'm Jordan, welcome to my github!

📨 jordanbott.dev@gmail.com <br/>
🗓️ [Meet with me!](https://calendly.com/jordanbott-dev/30min?back=1&month=2024-02) <br/>
📝 Check out my <a href="./Jordan%20Bott%20Resume.pdf" target="_blank">resume</a>! <br/>


<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

# Let's play <img src="./wordle/tiles/yellow/W.svg" width="28" /><img src="./wordle/tiles/green/O.svg" width="28" /><img src="./wordle/tiles/grey/R.svg" width="28" /><img src="./wordle/tiles/grey/D.svg" width="28" /><img src="./wordle/tiles/green/L.svg" width="28" /><img src="./wordle/tiles/grey/E.svg" width="28" />

 ![Static Badge](https://img.shields.io/badge/Total%20Players-{lifetime_data["players"]}-mediumpurple?style=flat&labelColor=lavender)  ![Static Badge](https://img.shields.io/badge/Total%20Wins-{lifetime_data["wins"]}-darkseagreen?style=flat&labelColor=ecfbe3) ![Static Badge](https://img.shields.io/badge/Total%20Games-{lifetime_data["games_played"]}-khaki?style=flat&labelColor=lightyellow) ![Static Badge](https://img.shields.io/badge/Total%20Moves-{lifetime_data["moves_made"]}-pink?style=flat&labelColor=lavenderblush)

> [!TIP]
> Everyone is welcome to participate! This is an **asynchronous**, and **collaborative** version of wordle, where players make one move at a time. Please make as many or as few moves as you would like!

Is this your first time here? Check out &ensp; [![Static Badge](https://img.shields.io/badge/HOW%20TO%20PLAY-darkseagreen?style=flat)](./wordle/HowToPlay.md)

We won! 🎉 The word was: {wordle_word}

Click "start a new game" to play again! ⬇️

[![Static Badge](https://img.shields.io/badge/START%20A%20NEW%20GAME-mediumpurple?style=flat)](https://github.com/jordan-bott/jordan-bott/issues/new?assignees=&labels=&projects=&template=wordle_guess.md&title=wordleguess%7C%5BPUT+5+LETTER+WORD+HERE%5D)

🧑‍💻 Most Recent Player:  &ensp; [![static badge](https://img.shields.io/badge/{shield_user}-burlywood?logo=github)](https://github.com/{user})


| Current Game | Letters |
| ------------ | ------- |
| {game_data["schema"]} | {letter_schema} |

Do you love stats? Check out these: &ensp; [![Static Badge](https://img.shields.io/badge/PLAYER%20STATS-darkseagreen?style=flat)](./wordle/stat_sheets/PlayerData.md) &nbsp;  [![Static Badge](https://img.shields.io/badge/GLOBAL%20STATS-darkseagreen?style=flat)](./wordle/stat_sheets/GlobalData.md)

"""

    file = open("README.md", "w")
    file.write(readme_content)
    file.close()

    new_game_data()
