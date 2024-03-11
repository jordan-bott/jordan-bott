from game_data import game_data


def update_readme():

    letter_schema = str(game_data["letter_schema"])

    readme_content = f"""
Hi! 👋🏼 I'm Jordan, welcome to my github!

📨 jordanbott.dev@gmail.com <br/>
🗓️ [Meet with me!](https://calendly.com/jordanbott-dev/30min?back=1&month=2024-02) <br/>
📝 Check out my <a href="./Jordan%20Bott%20Resume.pdf" target="_blank">resume</a>! <br/>


<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

Let's play wordle! Everyone is welcome to participate!

Click "make a guess" below to contribute.

The game is on guess # {game_data["turn_number"]}

[MAKE A GUESS](https://github.com/jordan-bott/jordan-bott/issues/new?assignees=&labels=&projects=&template=wordle_guess.md&title=wordleguess%7C%5BPUT+5+LETTER+WORD+HERE%5D)

| Current Game | Letters |
| ------------ | ------- |
| {game_data["schema"]} | {letter_schema} |

"""

    file = open("README.md", "w")
    file.write(readme_content)
    file.close()
