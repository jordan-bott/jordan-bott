from game_data import game_data
from new_letter_schema import new_letter_schmea
from new_game_data import new_game_data
import json


def handle_lose(wordle_word):

    letter_schema = "".join(new_letter_schmea)

    readme_content = f"""
Hi! 👋🏼 I'm Jordan, welcome to my github!

📨 jordanbott.dev@gmail.com <br/>
🗓️ [Meet with me!](https://calendly.com/jordanbott-dev/30min?back=1&month=2024-02) <br/>
📝 Check out my <a href="./Jordan%20Bott%20Resume.pdf" target="_blank">resume</a>! <br/>


<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

Let's play wordle! Everyone is welcome to participate!

We lost this one 🥲. The word was: {wordle_word}

Click "start a new game" to try again!

[START A NEW GAME](https://github.com/jordan-bott/jordan-bott/issues/new?assignees=&labels=&projects=&template=wordle_guess.md&title=wordleguess%7C%5BPUT+5+LETTER+WORD+HERE%5D)

| Current Game | Letters |
| ------------ | ------- |
| {game_data["schema"]} | {letter_schema} |

"""

    file = open("README.md", "w")
    file.write(readme_content)
    file.close()

    new_game_data()
