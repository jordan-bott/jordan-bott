# Asynchronous/Collaborative Wordle on Github!

Welcome to the ReadMe! If you have any questions about anything in here, please feel free to reach out [jordanbott.dev@gmail.com](jordanbott.dev@gmail.com)

If you've played, you've probably noticed that my version of wordle doesn't play quite like the [NYT version](https://www.nytimes.com/games/wordle/index.html) does. Rather than everyone in the world playing their own game with the same word, everyone plays in one game instance, one move at a time. Players are welcomed to make multiple moves in a row, or play one move and wait for the community to continue the game. Player and global stats are tracked, and can be found by looking at the [PLAYER STATS](./wordle/stat_sheets/PlayerData.md) and the [GLOBAL STATS](./wordle/stat_sheets/GlobalData.md). Only the player's github username is stored with their play stats.

## Overview

From a high level, the flow of the game is relatively straight forward:

- User submits guess through a GitHub issue
- GitHub Workflow is triggered Python Code Runs
- New commit is pushed to repository
- Issue is closed

## Table of Contents

1. [Explanation of Code](#explaination-of-code)
    - [Python Code (Game Logic)](#python-code-game-logic)
    - [GitHub Workflow](#github-workflow)
2. [Future of Project](#future-of-project)
    - [Feature Ideas](#feature-ideas)
    - [Bugs to Fix](#bugs-to-fix)
3. [Acknowledgements](#acknowledgements)


## Explaination of Code

In this section, I'll go through the logic of the code, and share some resources. Please do not hesitate to reach out if you have any questions, or think there are some sections that could use more clarity!

### Python Code (Game Logic)

*coming soon!*

### GitHub WorkFlow

*coming soon!*

## Future of Project

In this section I will share any future feature ideas that I have, as well as any bugs that have come up. If you notice a bug, or have a feature idea, please send me an email ([jordanbott.dev@gmail.com](jordanbott.dev@gmail.com))!

### Feature Ideas

- Further stat tracking
- Adjusting letter section to be styled more like a keyboard
- Adding shield.io images for stats

### Bugs to Fix

- Letters that exist in the word in more than one location do not display properly.
    - Ex. In the guess "latte" for the word "lathe", you will see a schema like this: 🟩🟩🟩🟨🟩 .<br /> However, the second `t` should be black as the `t` has been placed, and there are not two `t` in the word.

## Acknowledgements
- My idea for this project came from seeing [Jonathan Gin's](https://github.com/JonathanGin52) epic connect4 game 🎲
- A list of other cool GitHub profiles can be found [here](https://github.com/abhisheknaiidu/awesome-github-profile-readme?tab=readme-ov-file)!
