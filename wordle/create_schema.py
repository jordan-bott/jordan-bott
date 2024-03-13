from letter_indicies import letter_indicies
from game_data import game_data


def create_schema(wordle_word, guess):
    schema = ["", "", "", "", ""]
    letter_schema = game_data["letter_schema"]
    schema_key = ["", "", "", "", ""]

    # check for all of the greens from the guess
    for i in range(0, 5):
        letter = guess[i]
        if wordle_word[i] == letter:
            schema[i] = f'<img src="./wordle/tiles/green/{letter}.svg" width="40" />'
            letter_schema[letter_indicies[letter]] = (
                f'<img src="./wordle/letters/green/{letter}.svg" width="20" />'
            )
            schema_key[i] = "G"

    # check for yellows and greys
    for j in range(0, 5):
        letter = guess[j]
        if letter not in wordle_word:
            schema[j] = f'<img src="./wordle/tiles/grey/{letter}.svg" width="40" />'
            letter_schema[letter_indicies[letter]] = (
                f'<img src="./wordle/letters/grey/{letter}.svg" width="20" />'
            )
            schema_key[j] = "B"
        elif letter in wordle_word and letter != wordle_word[j]:
            # find indexes of the letter in the wordle word
            letter_index_list = []
            letter_count = wordle_word.count(letter)

            # figure out what indices the letter is found at
            wordle_word_copy = wordle_word
            for _ in range(letter_count):
                index = wordle_word_copy.find(letter)
                letter_index_list.append(index)
                wordle_word_copy = wordle_word_copy.replace(letter, "+", 1)

            # count how many of that letter are already in the right place
            found_green_letter_count = 0
            for index in letter_index_list:
                if schema_key[index] == "G":
                    found_green_letter_count += 1

            # determine if all of that letter are in the correct place
            # if they are not, add a yellow
            if letter_count != found_green_letter_count:
                schema[j] = f'<img src="./wordle/tiles/yellow/{letter}.svg" width="40" />'
                # if none of the right locations have been found, the keyboard should show
                # the letter as yellow
                if found_green_letter_count == 0 and letter_schema[letter_indicies[letter]] != f'<img src="./wordle/letters/green/{letter}.svg" width="20" />':
                    letter_schema[letter_indicies[letter]] = (
                        f'<img src="./wordle/letters/yellow/{letter}.svg" width="20" />'
                    )
                # if any of the locations of the letter have been found, the keyboard should
                # show the letter as green
                elif found_green_letter_count >= 1:
                    letter_schema[letter_indicies[letter]] = (
                        f'<img src="./wordle/letters/green/{letter}.svg" width="20" />'
                    )
                schema_key[j] = "Y"
            # if they are all in the correct place, add a grey
            else:
                schema[j] = f'<img src="./wordle/tiles/grey/{letter}.svg" width="40" />'
                # if they are all found, the keyboard should show green, but the schema should show
                # grey for the extra places
                letter_schema[letter_indicies[letter]] = (
                    f'<img src="./wordle/letters/green/{letter}.svg" width="20" />'
                )
                schema_key[j] = "B"

    # turn schema back into a string, and add a line break
    schema_str = "".join(schema)
    schema_str += "<br/>"
    return [schema_str, letter_schema]
