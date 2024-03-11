from letter_indicies import letter_indicies
from game_data import game_data

def create_schema(wordle_word, guess):
    schema = ""
    letter_schema = game_data["letter_schema"]

    for i in range(0, 5):
        if wordle_word[i] == guess[i]:
            schema += f'<img src="./wordle/tiles/green/{guess[i]}.svg" width="40" />'
            letter_schema[letter_indicies[guess[i]]] = f'<img src="./wordle/letters/green/{guess[i]}.svg" width="20" />'
        elif guess[i] in wordle_word:
            schema += f'<img src="./wordle/tiles/yellow/{guess[i]}.svg" width="40" />'
            letter_schema[letter_indicies[guess[i]]] = f'<img src="./wordle/letters/yellow/{guess[i]}.svg" width="20" />'
        else:
            schema += f'<img src="./wordle/tiles/grey/{guess[i]}.svg" width="40" />'
            letter_schema[letter_indicies[guess[i]]] = f'<img src="./wordle/letters/grey/{guess[i]}.svg" width="20" />'
    schema += "<br/>"
    return [schema, letter_schema]
