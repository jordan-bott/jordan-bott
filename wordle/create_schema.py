def create_schema(wordle_word, guess):
    schema = ""
    for i in range(0, 5):
        if wordle_word[i] == guess[i]:
            schema += f'<img src="./wordle/tiles/green/{guess[i]}.svg" width="40" />'
        elif guess[i] in wordle_word:
            schema += f'<img src="./wordle/tiles/yellow/{guess[i]}.svg" width="40" />'
        else:
            schema += f'<img src="./wordle/tiles/grey/{guess[i]}.svg" width="40" />'
    schema += "<br/>"
    return schema


create_schema('HELLO', 'PLANT')
