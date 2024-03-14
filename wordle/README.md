# Asynchronous/Collaborative Wordle!

Welcome to the ReadMe! If you have any questions about anything in here, please feel free to reach out - [jordanbott.dev@gmail.com](jordanbott.dev@gmail.com)

If you've played, you've probably noticed that my version of wordle doesn't play quite like the [NYT version](https://www.nytimes.com/games/wordle/index.html) does. Rather than everyone in the world playing their own game with the same word, everyone plays in the same game, and plays one move at a time. Players are welcomed to make multiple moves in a row, play one move and wait for the community to continue the game, or anything in between! Unlike the NTY wordle, every time a game completes, a new word is ready! Player and global stats are tracked, and can be found by looking at the [PLAYER STATS](./stat_sheets/PlayerData.md) and the [GLOBAL STATS](./stat_sheets/GlobalData.md). Only the player's github username is stored with their play stats.

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
    - [Bugs](#bugs-🐛🐞🐜)
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

There are multiple python files used in this project (18 of them!), however only `main.py` is triggered by the workflow. I view `main.py` like a control center. It is taking in data and deciding where it should go - what path it should follow. To keep this file more succinct and easy to read, `main.py` calls functions in other files to handle specific steps in the process. Below I will go through the functions/uses of each file individually.

⚠️ With the excpetion of `main.py` all files are discussed in alphabetical order (how they appear in the file tree), and are not in the order they are triggered or accessed by `main.py`.

Feel free to skip to a specific file's explanation here:
|   |   |   |
| - | - | - |
|[main.py](#📄-mainpy) |  [check_word_validity.py](#📄-check_word_validitypy) |  [create_schema.py](#📄-create_schemapy)  |
| [game_data.py](#📄-game_datapy) | [handle_global_stats.py](#📄-handle_global_statspy) |[handle_invalid_guess.py](#📄-handle_invalid_guesspy) |
| [handle_lose.py](#📄-handle_losepy) | [handle_player_stats.py](#📄-handle_player_statspy) | [handle_win.py](#📄-handle_winpy) |
| [letter_indicies.py](#📄-letter_indiciespy) |[lifetime_data.py](#📄-lifetime_datapy) | [new_game_data.py](#📄-new_game_datapy) |
|  [new_letter_schema.py](#📄-new_letter_schemapy) | [player_data.py](#📄-player_datapy) | [possible_words.py](#📄-possible_wordspy) |
| [update_lifetime_data.py](#📄-update_lifetime_datapy) | [update_player_data.py](#📄-update_player_datapy) | [update_readme.py](#📄-update_readmepy) |


#### 📄 `main.py`

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

#### 📄 `check_word_validity.py`

You can view `check_word_validity.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/check_word_validity.py)

The purpose of the `check_word_validity` function is to check that the guess is a valid wordle guess. To do this, we check a few things. If all checks pass, `check_word_validity` will return `True`. This is used in `main.py` to determine stat saving and the rendering of the ReadMe. If any single check fails, `check_word_validity` will return `False`.

1. Check if the guess is 5 letters long. This double checks that the guess grabbed from the title of the issue is exactly 5 characters long. Because we index the title to grab the guess, the guess is almost certainly 5 characters, however this serves as a way to double check! If the guess is not exactly 5 letters, `check_word_validity` returns `False` and "Please guess a 5 letter word" is printed to the workflow's logs.

2. Checks if the guess has been guessed already this game. A list of guessed words for this game is stored in `[game_data.py`](#📄-game_datapy). The guess is checked against this list to determine if it has been guessed already, if it has, `check_word_validity` returns `False` and "You've already guess that one!" is printed to the workflow's logs.

3. Checks if the guess is in the disallowed words list. As this is a professional space, I have a hidden list of words that are inappropriate, offensive, or unprofessional. This check makes sure the guess is not found in this list. If it is found in this list, `check_word_validity` returns `False`, and "Hmm that word isn't allowed. Please be respectful/appropriate with your guess" is printed to the workflow's logs.

4. Checks if the guess is found within the dictionary. Players may only guess actual words (i.e. qwerty is not a valid guess), so [Free Dictionary API](https://dictionaryapi.dev/) is used to check if the guess can be found in the dictionary. If the guess is found in the dictionary, a list is returned. If it is not found in the dictionary a dictionary is returned. This check makes sure than a list is returned, if a dictionary has been returned `check_word_validity` will return `False` and "Whoops, that word isn't in the dictionary" is printed to the workflow's logs. Occasionally, the API returns None. If this happens, `check_word_validity` returns `False` and "Bad API response" is printed to the workflow's logs.

After these 4 checks, the code knows the word is a valid guess! `check_word_validity` will return `True`.


#### 📄 `create_schema.py`

You can view `create_schema.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/create_schema.py).

This file contains the most complex logic of the whole project, as it is what determines if a letter should be yellow, green, or gray. At first, I thought this was pretty straight forward. If the letter matches the letter in that spot, it's green (`guess[i] == wordle_word[i]`). The greens are nice and straight forward like this! The grays are also straight forward. If the letter cannot be found anywhere in the wordle word (`letter not in wordle_word`), the letter should be gray.

The logic of the yellows gets a bit more complex. Originally I thought if the letter is somewhere in the wordle word, and it is not in that spot (`guess[i] != wordle_word[i] and guess[i] in wordle_word`) then the letter should be yellow. However let's consider the following scenario:

Wordle Word: LATHE

Guess: LATTE

With this wordle word and guess, along with our previous simple logic it would produce a schema like this:

<img src="./tiles/green/L.svg" width="20" /><img src="./tiles/green/A.svg" width="20" /><img src="./tiles/green/T.svg" width="20" /><img src="./tiles/yellow/T.svg" width="20" /><img src="./tiles/green/E.svg" width="20" />

This doesn't make a lot of sense, because it implies that there is another "T" somewhere, but there is nowhere to place it. Instead, the schema should look like this:

<img src="./tiles/green/L.svg" width="20" /><img src="./tiles/green/A.svg" width="20" /><img src="./tiles/green/T.svg" width="20" /><img src="./tiles/grey/T.svg" width="20" /><img src="./tiles/green/E.svg" width="20" />

To do this, we have to check for a few other conditions, such as how many times the letter appears in the wordle word, and if those letters are already in the correct place. We only want to show yellow tiles if there is still a remaining spot that is missing that letter (not green).

For example, when using the wordle word "TEACH" and the guess "LATTE". We do want both "T" in latte to be yellow, because both of those locations for "T" are not correct in LATTE, but there is a "T" in TEACH.

To help track this, I use a variable `schema_key` which is just a list that tracks "G" for green (meaning a green tile is there), "Y" for yellow, and "B" for gray (green also starts with G, so I went with B for black).

-> Check for all of the Greens

First I will loop through the guess and place all of the greens into the schema. I store the schema as a list so I can easily insert into the index they belong in. I insert the image for the wordle tile into the schema list, update the keyboard letter tile to be green, and set the schema key to "G" at that index. This information will be helpful later when determining yellow tiles.

-> Check for Yellows and Grays

I then loop through the guess again to determine gray and yellow tiles. As I mentioned before, gray is easy as it is a conditional check to see if the letter is not in the word. If it's not, I add the image for the gray tile to the schema list, turn the keyboard letter to gray, and update the schema key to "B" for that index.

If the letter is in the word, and it's not the correct letter for that spot (i.e. it could be yellow), I will find all of the indexes where the letter is found in the wordle word. I do this by using the `.count()` method on the wordle word, and then looping the amount of times the letter is found. In this loop, I will use the `.find()` method to determine where the nearest index to the start that is the letter is, and store that index. Because `.find()` will only find the first index of the letter, I replace that instance of the letter with a `+` so that the next time through the loop will find the next index of the letter.

Now that we have a list of all the indexes where the letter is found in the wordle word we want to count how many of those indexes are green (have the correct letter in the guess for the wordle word). To do this, I loop through the list of indexes and see if the `schema_key` has `"G"` at that index. If it does, I add one to my `found_green_letter_count`.

If we have more instances of the letter than we found green, we know we want this instance of the letter to be yellow (there are still more places to put the letter, but this place isn't right). So, we will add the yellow tile image to the schema. However, if there are any green instances of the letter, we want the keyboard to show it as green. So we will check if the letter schema already shows green (from a past guess) and/or if the current guess already has a green for this letter. If both of those are not true, we can turn the keyboard yellow for this letter.

If the number of occurances of the letter in the word, and the number of greens we have are equal, then we have found all of the locations for that letter! Since this letter is not in the right place, and there are no missing locations for it, it should show gray in this schema, and the keyboard should show green for the letter.

-> Finish up and reformat

Now that the schema is fully built, we want to turn the schema into a string, and add "</br>" so it will properly show in the readme!

#### 📄 `game_data.py`

You can view `game_data.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/game_data.py).

I have several files in this repo that keep track of data long term. There were a few ways to do this (json, yml, md, etc.), but I decided to keep it in pure python. The purpose of `game_data.py` is to keep track of the current game's data. This is important as the script is ran every time that there is a new guess, if we didn't track the index of the wordle word, the schema, and some other key items the game would "reset" every time there was a new guess - which is not the behavior that we want.

`game_data.py` contains only a dictionary called `game_data` that keeps track of the following data:

- `wordle_index` (string)
    - I have chosen to track the wordle index so that the actual wordle word is not revealed in the code. While someone could theorhetically find the wordle word based on it's index, this makes it a few more steps and will hopefully deter most cheating. The index corresponds to a list of possible words found in `possible_words.py`. At the beginning of the script, the code will assign the wordle word using the `possible_words` list, and the index stored here.
- `turn_number` (integer)
    - Tracking the turn number is important to determine when the end of the game is. The game ends when either the wordle word is guessed, or the community has made 6 guesses. When the turn number is 6 (`turn_number == 6`) the game will trigger a loss.
- `guessed_words` (list)
    - Guessed words are tracked to be used in [`check_word_validity.py`](#📄-check_word_validitypy). If a word has already been guessed this game, we don't want to use a turn guessing it again, so the code will determine that guess to be invalid.
- `players` (list)
    - A list of players is tracked to keep track of which players have participated in the current game. This list will have use in future features!
- `schema` (string)
    - The schema string keeps a string of all of the image tags to be added to the ReadMe and is created in [`create_schema.py`](#📄-create_schemapy). The schema is the letter tiles used to show the yellows, greens, and grays for a guess.
- `letter_schema` (list)
    - The letter schema is what is used to produce the keyboard next to the game that displays if a particular letter has is green/yellow/gray/unguessed in the game. The letter schema is edited in [`create_schema.py`](#📄-create_schemapy).


#### 📄 `handle_global_stats.py`

You can view `handle_global_stats.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/handle_global_stats.py).

This file has one function `handle_global_stats()`, and handles updating the [`GlobalData.md`](./stat_sheets/GlobalData.md) file. The file is relatively straight forward, simply parsing information from [`lifetime_data`](#📄-lifetime_datapy) into a table inside of a string to write into the GlobalData file. There is also a `for` loop to determine the most guessed word.

#### 📄 `handle_invalid_guess.py`

You can view `handle_invalid_guess.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/handle_invalid_guess.py)

This file will update the readme with the "invalid guess" look if a guess is determined to be invalid by [`check_word_validity.py`](#📄-check_word_validitypy). The file edits the user's username to fit the shield url requirements ("-" should be "--", "_" should be "__") and joins the `letter_schema` from `game_data` into a string to display on the readme. The file then rewrites the readme with the new content. If triggered, this is returned from `main.py` and thus ends the python section of code.

#### 📄 `handle_lose.py`

You can view `handle_lose.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/handle_lose.py).

This file is triggered when the game has hit 6 guesses, and the wordle word has not been guessed. The file edits the user's username to fit the shield url requirements ("-" should be "--", "_" should be "__") and joins the `letter_schema` from `game_data` into a string to display on the readme. The file then rewrites the readme with the new content specifying that the game has been lost. Finally it runs [`new_game_data.py`](#📄-new_game_datapy). If triggered, this is returned from `main.py` and thus `new_game_data.py` ends the python section of code.

#### 📄 `handle_player_stats.py`

You can view `handle_player_stats.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/handle_player_stats.py).

This file is used to create the [Player Data Stat Sheet](./stat_sheets/PlayerData.md). It has one function `handle_player_stats()` which uses a `for` loop to build a string that is then displayed in the markdown file. After creating the table in the `table_content` string it will rewrite the `PlayerData.md` file to include the new table. Because of this, after every move the entire `PlayerData.md` table is recreated and rewritten.

#### 📄 `handle_win.py`

You can view `handle_win.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/handle_win.py).

This file is triggered when the wordle word has been guessed. The file edits the user's username to fit the shield url requirements ("-" should be "--", "_" should be "__") and joins the `letter_schema` from `game_data` into a string to display on the readme. The file then rewrites the readme with the new content specifying that the game has been won. Finally it runs [`new_game_data.py`](#📄-new_game_datapy). If triggered, this is returned from `main.py` and thus `new_game_data.py` ends the python section of code.

#### 📄 `letter_indicies.py`

You can view `letter_indicies.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/letter_indicies.py).

This file is very simple. It is holding a dictionary that does not change of what index each of the letters can be found at for the letter schema. This is so that the letters in the `letter_schema` can be in QWERTY order, and I can include `<br / >` tags appropriately. This file is used in [`create_schema.py`](#📄-create_schemapy) to know which item in the `letter_schema` list to change when looking at each letter of the guess.

#### 📄 `lifetime_data.py`

You can view `lifetime_data.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/lifetime_data.py).

`lifetime_data.py` is one of 3 files in this repo that are used to track data long term (see also: [`game_data.py](#📄-game_datapy) and [`player_data.py`](#📄-player_datapy)). Long term meaning, longer than the run time of the script. In this file, we are tracking "all time" stats. These are not specific to any one player or any one game, and serve as a culmination of all guesses and games. Stats have been tracked since March 10, 2024.

This file contains a dictionary called `lifetime_data` and it tracks the following information:

- `moves_made` (integer)
    - This is the total moves (guesses) made.
- `games_played` (integer)
    - Total completed games
- `players` (integer)
    - Total *unique* players participated
- `wins` (integer)
    - Total number of games played resulting in a win
- `losses` (integer)
    - Total number of games played resulting in a loss
- `invalid_guesses` (integer)
    - Total number of invalid guesses made
- `words_guessed` (dictionary)
    - A dictionary of all guessed words as the key, and the number of times they have been guessed as the value. This is used to determine the most guessed word.
- `wordle_words` (list)
    - This list tracks all past wordle words, in order.


#### 📄 `new_game_data.py`

You can view `new_game_data.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/new_game_data.py).

This file contains one function `new_game_data()`. The purpose of `new_game_data()` is to reset the game data back to the "new" state after a game has concluded. This is called by [`handle_win.py`](#📄-handle_winpy) and [`handle_lose.py`](#📄-handle_losepy) to ready [`game_data.py`](#📄-game_datapy) for a new game!

It contains a dictionary `game_data` with the "reset" or "new" game data, and then rewrites [`game_data.py`](#📄-game_datapy) with this dictionary.

#### 📄 `new_letter_schema.py`

You can view `new_letter_schema.py` [here](https://github.com/jordan-bott/jordan-bott/blob/main/wordle/new_letter_schema.py).

This file just contains one list called `new_letter_schema`, which is a list of all the keyboard letter images in white (their default "new game" state). This list is used by [`new_game_data.py`](#📄-new_game_datapy) to give [`game_data.py`](#📄-game_datapy) a reset keyboard for the new game.

#### 📄 `player_data.py`

*coming soon!*

#### 📄 `possible_words.py`

*coming soon!*

#### 📄 `update_lifetime_data.py`

*coming soon!*

#### 📄 `update_player_data.py`

*coming soon!*

#### 📄 `update_readme.py`

*coming soon!*

## Future of Project

In this section I will share any future feature ideas that I have, as well as any bugs that have come up. If you notice a bug, or have a feature idea, please send me an email ([jordanbott.dev@gmail.com](jordanbott.dev@gmail.com))!

### Future Feature Ideas

- Further stat tracking
- Adjusting letter section to be styled more like a keyboard
- Auto show game schema and letters in the issue template
- Further error handling to update the ReadMe should something bad happen in the workflow
- Email sent to players who have participated after the game is complete

### Bugs 🐛🐞🐜

- ✅ Solved: Letters that exist in the word in more than one location do not display properly.
    - Ex. In the guess "latte" for the word "lathe", you will see a schema like this: 🟩🟩🟩🟨🟩 .<br /> However, the second `t` should be black as the `t` has been placed, and there are not two `t` in the word.

## Acknowledgements
- My idea for this project came from seeing [Jonathan Gin's](https://github.com/JonathanGin52) epic connect4 game 🎲
- A list of other cool GitHub profiles can be found [here](https://github.com/abhisheknaiidu/awesome-github-profile-readme?tab=readme-ov-file)!
