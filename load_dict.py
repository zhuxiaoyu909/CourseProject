import requests
import json



def api_request(word):
    """
    api_request pull the word definition from API.

    :param word: the english word user wants to search
    :return: list of tuple containing POS tags and definitions
    """
    base_url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    response_api = requests.get(base_url + str(word).lower())
    contents = json.loads(response_api.text)

    meanings = []
    if isinstance(contents, dict):
        meanings.append((contents['title'], contents['message']))
    else:
        for content in contents[0]['meanings']:
            key_to_check = "partOfSpeech"
            if key_to_check not in content.keys():
                content[key_to_check] = 'N/A'
                
            meanings.append((content[key_to_check], content['definitions'][0]['definition']))

    return meanings


def word_def(word):
    """
    word_def pull the word definition from word_def.Json.
    If the word is not presented, then pull the definition
    through API request.

    :param word: the english word user wants to search
    :return: list of tuple containing POS tags and definitions
    """
    word_lower = str(word).lower()
    with open('data/word_def.json', "r") as f:
        frequent_word_def = json.load(f)

    if word_lower.isalpha():
        word_meaning = frequent_word_def[word_lower] if word_lower in frequent_word_def.keys() else api_request(word_lower)
    else:
        word_meaning = [('Invalid input', 'N/A')]
    return word_meaning


if __name__ == '__main__':
    print(word_def('Phenomenon'))
