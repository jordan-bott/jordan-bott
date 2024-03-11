# Asynchronous/Collaborative Wordle!

Welcome to the ReadMe! If you have any questions about anything in here, please feel free to reach out - [jordanbott.dev@gmail.com](jordanbott.dev@gmail.com)

If you've played, you've probably noticed that my version of wordle doesn't play quite like the [NYT version](https://www.nytimes.com/games/wordle/index.html) does. Rather than everyone in the world playing their own game with the same word, everyone plays in the same game, and plays one move at a time. Players are welcomed to make multiple moves in a row, or play one move and wait for the community to continue the game. Unlike the NTY wordle, every time a game completes, a new word is ready! Player and global stats are tracked, and can be found by looking at the [PLAYER STATS](./wordle/stat_sheets/PlayerData.md) and the [GLOBAL STATS](./wordle/stat_sheets/GlobalData.md). Only the player's github username is stored with their play stats.

## Overview

From a high level, the flow of the game is relatively straight forward:

- User submits guess through a GitHub issue
- GitHub Workflow is triggered Python Code Runs
- New commit is pushed to repository
- Issue is closed

## Table of Contents

1. [Explanation of Code](#explaination-of-code)
    - [GitHub Workflow](#github-workflow)
    - [Python Code (Game Logic)](#python-code-game-logic)
2. [Future of Project](#future-of-project)
    - [Feature Ideas](#feature-ideas)
    - [Bugs to Fix](#bugs-to-fix)
3. [Acknowledgements](#acknowledgements)


## Explaination of Code

In this section, I'll go through the logic of the code, and share some resources. Please do not hesitate to reach out if you have any questions, or think there are some sections that could use more clarity!

### GitHub WorkFlow

The magic of this code, lies mainly in the GitHub Workflow. The Workflow manages the automation of many aspects of the game, including commiting and pushing any file changes to the repo automatically. The python code handles the logic of the game and the writing of the files, however the workflow triggers the python code, grabs information from the GitHub issue.

The workflow can be found [here](https://github.com/jordan-bott/jordan-bott/blob/main/.github/workflows/wordle.yml) for reference!

#### Jobs

There are two jobs ran within this workflow: `wordle-guess` and `udpate-waka`. `wordle-guess` handles all of the game logic, committing and pushing any wordle changes to the repository. `update-waka` is ran to re-add my waka stats to my readme, as these are erased when rewriting the readme during `wordle-guess`. Because of this, I will just go through the `wordle-guess` job.

#### wordle-guess

After the workflow is triggered by opening an issue, `wordle-guess` checks to see if the issue starts with `wordleguess|` (line 10). If so, it will continue through the job, if not the job is skipped.

The job begins by checking out the repo so the workflow can access the repo (step: `Checkout`). Then it will setup the python environment and install any dependencies (steps: `Python Setup` & `Install Python Dependencies`).

The next step is `Handle Move`. This is where all of the game logic and all edits to involved markdown files occurs. It does this by running `python wordle/main.py`. More discussion of what happens in `main.py` [here](#python-code-game-logic). After this it will run `black wordle/` to reformat the data files back into readable python code, as the `write` method of `open()` pastes the file contents in one line (unless specified otherwise).

Next, it will automatically create a commit for the changes made by `main.py` (step: `Commit Files`) and push those changes to the repo (step: `Push Changes`). This is important because `main.py` is editing several files and we want to see those changes automatically show up on the profile page without any more user input.

Finally, the `Close Issue` step will close the issue that was opened and triggered this workflow. This is done by using the GitHub CLI and running `gh issue close ${{github.event.issue.number}}` (line 59). While not a necessary step, this is a nice housekeeping step as the issues are used to trigger the workflow, and pass in the guess, but are not needed after the workflow has been ran. Information about the GitHub CLI can be found [here](https://cli.github.com/manual/gh_issue_close)

### Python Code (Game Logic)

There are multiple python files used in this project (18 of them!), however only `main.py` is triggered by the workflow. I view `main.py` like a control center. It is taking in data and deciding where it should go - what path it should follow. To keep this file more succinct and easy to read, `main.py` calls functions in other files to handle specific steps in the process. Below I will go through the functions/uses of each file individually:

Feel free to skip to a specific file's explanation here:
|   |   |   |
| - | - | - |
|[main.py](#mainpy) |  [check_word_validity.py](#check_word_validitypy) |  [create_schema.py](#create_schemapy)  |
| [game_data.py](#game_datapy) | [handle_global_stats.py](#handle_global_statspy) |[handle_invalid_guess.py](#handle_invalid_guesspy) |
| [handle_lose.py](#handle_losepy) | [handle_player_stats.py](#handle_player_statspy) | [handle_win.py](#handle_winpy) |
| [letter_indicies.py](#letter_indiciespy) |[lifetime_data.py](#lifetime_datapy) | [new_game_data.py](#new_game_datapy) |
|  [new_letter_schema.py](#new_letter_schemapy) | [player_data.py](#player_datapy) | [possible_words.py](#possible_wordspy) |
| [update_lifetime_data.py](#update_lifetime_datapy) | [update_player_data.py](#update_player_datapy) | [update_readme.py](#update_readmepy) |


#### `main.py`

You can view `main.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/main.py)

As I mentioned, this is control center of the whole process. `main.py` is triggered by the GitHub Workflow. The main purpose of `main.py` is to direct traffic, and determine which steps in the process we should follow based on the input. For example, if the guess is determined to be an invalid guess (not a word found in the dictionary, or an already guessed word), `main.py` will trigger a different function to update the README than if the guess *is* valid.

While `main.py` is one file (one function), I have broken it up into different sections:

**-> Check if there is a wordle index**

First we will check if there is a `wordle_index` stored in the `game_data.py` file. This `wordle_index` is how I keep track of if we are in a current game, or need to start a new game. If this is blank, we should start a new game by assigning a random integer between 0 and 2314 to `wordle_index`. When a game is won or lost, the `wordle_index` will be reset to an empty string.

**-> Pull Wordle Word Based on Wordle Index**

Now that there is a `wordle_index` assigned in the game data, we will use that to grab the wordle word. I opted to store an index rather than the word itself to make it more difficult to search for the answer in the source code as a player. `possible_words.py` holds a function that returns a list of all possible words, and this is indexed at `wordle_index` to grab the current game's word.

**-> Pull Guess From Issue Meta Data**

This is where the GitHub issue comes into play. The GitHub issue serves two purposes: triggering the GitHub Workflow and providing the guess to the game. This is where we pull the guess from the title of the issue. In the [issue template](https://github.com/jordan-bott/jordan-bott/blob/main/.github/ISSUE_TEMPLATE/wordle_guess.md) there are instructions on exactly how to insert the guess so that the code correctly parses through it.

This information is pulled directly from the title of the issue and stored in an environment variable in the GitHub Workflow. Then in `main.py` it is stored in a variable to be used throughout the rest of the file.

**-> Pull User From Issue Meta Data**

This works identically to the above, and pulls the username of the user who submitted the issue and stores it as the `user` in `main.py`.  This is used to track player stats, and **only the username** of the user is stored (and of course their stats like how many games they've won, and how many guesses they've made!). The current game's data also stores a list of participating players, and that information is updated in this step as well.

**-> Check If Guess is Valid**

This step uses the [`check_word_validity`](#check_word_validitypy) function to determine if a guess is valid. If it is, it will update the game's data with the guess and continue through the next steps of `main.py`.

If the guess is not valid, player data is updated (using [`update_player_data`](#update_player_datapy)), lifetime stats are updated (using [`update_lifetime_data`](#update_lifetime_datapy)), and we return [`handle_invalid_guess`](#handle_invalid_guesspy), which updates the Readme with the information that the most recent guess was invalid. If this is triggered, the python code ends here, and the GitHub Workflow will continue through to commiting and pushing the code, closing the issue, and updating wakatime.

**-> Create Schemas**

This step uses [`create_schema`](#create_schemapy) to create both the past guess schema (this one: 🟩🟩⬛️🟨🟩), and what I've called the "letter schema" which is the letters to the side of the game, organized in a QWERTY keyboard layout to better visualize which letters have been used/unused. The [`create_schema`](#create_schemapy) function returns a list of these two schemas and they are stored into the current game's information.

**-> Update game_data**

Throughout `main.py` we have been updating game information. This has been stored in the `updated_game_data` variable, so that we only have to write to the `game_data.py` file once. At this point, we update the turn number, and can update [`game_data.py`](#game_datapy). We do this by using python's built in `open()` function, which allows us to open a file in our file tree, and then read, append or write to it. In this case, we will be writing to it, which will replace all exisiting information with our new game data. `open()` can only write strings, so we pass the game data in as json using `json.dumps`, however, the `game_data.py` file will interpret this as python once it's written.

**-> Check if Win & Update Player Meta Data**

Finally, after checking if the guess is valid, updating all kinds of data, and working through most of `main.py` we can check to see if we've won! This is a very simple conditional checking `if wordle_word == guess`. If this is true, we do a few things. First, we update the player data for the user who triggered the issue using [`update_player_data`](#update_player_datapy). Then we will update the lifetime data using [`update_lifetime_data`](#update_lifetime_datapy). Player data and lifetime data are used to create the stats pages ([player stats](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/stat_sheets/PlayerData.md) [global stats](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/stat_sheets/GlobalData.md)), this is done using [`handle_player_stats`](#handle_player_statspy) and [`handle_global_stats`](#handle_global_statspy) respectively.

Then a special rendering of the readme is produced by [`handle_win`](#handle_winpy) to show the winning game, and prompt users for a new game. This exits `main.py` and the GitHub workflow will continue onto it's next step.

**-> Check if Lose & Update Player Meta Data**

If we didn't win, perhaps we lost. So we will check that here. We do this by checking if the turn number stored in our game data is exactly equal to 6. If it is, we have taken the allotted amount of turns, and we lost. The process for a loss is similar to a win: we update the player data for the user who triggered the issue using [`update_player_data`](#update_player_datapy) and update the lifetime data using [`update_lifetime_data`](#update_lifetime_datapy).

Then a special rendering of the readme is produced by [`handle_lose`](#handle_losepy) to show the losing game and prompt users to start a new game. This exits `main.py` and the GitHub workflow will continue onto it's next step.

**-> Update Player Meta Data**

If we neither won nor loss, than the game continues! We will update the player data for the user who triggered the issue using [`update_player_data`](#update_player_datapy) and update the lifetime data using [`update_lifetime_data`](#update_lifetime_datapy) with information about the turn.

**-> Update Readme**

Finally, we will update the readme with the most recent guess using [`update_readme`](#update_readmepy), finishing the `main.py` process! The GitHub workflow will continue onto it's next step.

#### `check_word_validity.py`

*coming soon!*

#### `create_schema.py`

*coming soon!*

#### `game_data.py`

*coming soon!*

#### `handle_global_stats.py`

*coming soon!*

#### `handle_invalid_guess.py`

*coming soon!*

#### `handle_lose.py`

*coming soon!*

#### `handle_player_stats.py`

*coming soon!*

#### `handle_win.py`

*coming soon!*

#### `letter_indicies.py`

*coming soon!*

#### `lifetime_data.py`

*coming soon!*

#### `new_game_data.py`

*coming soon!*

#### `new_letter_schema.py`

*coming soon!*

#### `player_data.py`

*coming soon!*

#### `possible_words.py`

*coming soon!*

#### `update_lifetime_data.py`

*coming soon!*

#### `update_player_data.py`

*coming soon!*

#### `update_readme.py`

*coming soon!*

## Future of Project

In this section I will share any future feature ideas that I have, as well as any bugs that have come up. If you notice a bug, or have a feature idea, please send me an email ([jordanbott.dev@gmail.com](jordanbott.dev@gmail.com))!

### Feature Ideas

- Further stat tracking
- Adjusting letter section to be styled more like a keyboard
- Adding shield.io images for stats
- Auto show game schema and letters in the issue template
- Further error handling to update the ReadMe should something bad happen in the workflow

### Bugs to Fix

- Letters that exist in the word in more than one location do not display properly.
    - Ex. In the guess "latte" for the word "lathe", you will see a schema like this: 🟩🟩🟩🟨🟩 .<br /> However, the second `t` should be black as the `t` has been placed, and there are not two `t` in the word.

## Acknowledgements
- My idea for this project came from seeing [Jonathan Gin's](https://github.com/JonathanGin52) epic connect4 game 🎲
- A list of other cool GitHub profiles can be found [here](https://github.com/abhisheknaiidu/awesome-github-profile-readme?tab=readme-ov-file)!
