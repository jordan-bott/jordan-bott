from letter_indicies import letter_indicies
from game_data import game_data


def create_schema(wordle_word, guess):
    schema = ""
    letter_schema = game_data["letter_schema"]
    wordle_key = ["B", "B", "B", "B", "B"]

    for i in range(0, 5):
        letter = guess[i]
        if wordle_word[i] == letter:
            schema += f'<img src="./wordle/tiles/green/{letter}.svg" width="40" />'
            letter_schema[letter_indicies[letter]] = (
                f'<img src="./wordle/letters/green/{letter}.svg" width="20" />'
            )
            wordle_key[i] = "G"
        elif letter in wordle_word:
            instaces_of_letter = wordle_word.count(letter)
            indexes = []
            found_letter_count = 0
            for j in range(instaces_of_letter + 1):
                index = wordle_word.find(letter)
                indexes.append(index)
                wordle_word.replace(letter, "+", 1)
            for index in indexes:
                if wordle_key[index] == "G":
                    found_letter_count += 1
            if found_letter_count < instaces_of_letter:
                schema += f'<img src="./wordle/tiles/yellow/{letter}.svg" width="40" />'
                letter_schema[letter_indicies[letter]] = (
                    f'<img src="./wordle/letters/yellow/{letter}.svg" width="20" />'
                )
                wordle_key[i] = "Y"
            else:
                schema += f'<img src="./wordle/tiles/grey/{letter}.svg" width="40" />'
                letter_schema[letter_indicies[letter]] = (
                    f'<img src="./wordle/letters/grey/{letter}.svg" width="20" />'
                )
                wordle_key[i] = "B"
        else:
            schema += f'<img src="./wordle/tiles/grey/{letter}.svg" width="40" />'
            letter_schema[letter_indicies[letter]] = (
                f'<img src="./wordle/letters/grey/{letter}.svg" width="20" />'
            )
            wordle_key[i] = "B"
    schema += "<br/>"
    return [schema, letter_schema]
