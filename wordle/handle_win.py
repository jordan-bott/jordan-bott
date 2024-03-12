from game_data import game_data
from new_game_data import new_game_data
from lifetime_data import lifetime_data
import json


def handle_win(wordle_word, user):

    letter_schema = "".join(game_data["letter_schema"])

    readme_content = f"""
Hi! 👋🏼 I'm Jordan, welcome to my github!

📨 jordanbott.dev@gmail.com <br/>
🗓️ [Meet with me!](https://calendly.com/jordanbott-dev/30min?back=1&month=2024-02) <br/>
📝 Check out my <a href="./Jordan%20Bott%20Resume.pdf" target="_blank">resume</a>! <br/>


<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

# Let's play wordle! Everyone is welcome to participate!

 ![Static Badge](https://img.shields.io/badge/Total%20Players-{lifetime_data["players"]}-mediumpurple?style=flat&labelColor=lavender)  ![Static Badge](https://img.shields.io/badge/Total%20Wins-{lifetime_data["wins"]}-darkseagreen?style=flat&labelColor=ecfbe3) ![Static Badge](https://img.shields.io/badge/Total%20Games-{lifetime_data["games_played"]}-khaki?style=flat&labelColor=lightyellow) ![Static Badge](https://img.shields.io/badge/Total%20Moves-{lifetime_data["moves_made"]}-pink?style=flat&labelColor=lavenderblush)

We won! 🎉 The word was: {wordle_word}

Click "start a new game" to play again!

[START A NEW GAME](https://github.com/jordan-bott/jordan-bott/issues/new?assignees=&labels=&projects=&template=wordle_guess.md&title=wordleguess%7C%5BPUT+5+LETTER+WORD+HERE%5D)

Most Recent Player: [{user}](https://github.com/{user})

| Current Game | Letters |
| ------------ | ------- |
| {game_data["schema"]} | {letter_schema} |

Do you love stats? Check out these:
[PLAYER STATS](./wordle/stat_sheets/PlayerData.md)   [GLOBAL STATS](./wordle/stat_sheets/GlobalData.md)

"""

    file = open("README.md", "w")
    file.write(readme_content)
    file.close()

    new_game_data()
