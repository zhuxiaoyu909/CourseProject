import json
from typing import List
from nltk.stem.snowball import SnowballStemmer


class Definition(object):
    def __init__(self, pos, desc):
        self.pos = pos
        self.desc = desc

    def __str__(self):
        return f"POS: {self.pos}, Definition: {self.desc}"


class WordDefinition(object):
    def __init__(self, definitions: List[Definition]):
        self.definitions = definitions

    def __str__(self):
        return "\n".join([str(d) for d in self.definitions])

    def not_empty(self):
        return len(self.definitions) > 0


class WordDefinitions(object):
    def __init__(self, json_file_path: str):
        with open(json_file_path, "r") as f:
            self.word_def = json.load(f)
        self.stemmer = SnowballStemmer("english")

    def find_definition(self, word):
        word_lower = str(word).lower()
        word_stemmed = self.stemmer.stem(str(word))
        if word_lower in self.word_def:
            definition_arr = self.word_def[word_lower]
            definitions = [Definition(pos=d[0], desc=d[1]) for d in definition_arr]
            return WordDefinition(definitions=definitions)
        elif word_stemmed in self.word_def:
            definition_arr = self.word_def[word_stemmed]
            definitions = [Definition(pos=d[0], desc=d[1]) for d in definition_arr]
            return WordDefinition(definitions=definitions)
        else:

            return WordDefinition(definitions=[])


def test():
    word_def = WordDefinitions(json_file_path="data/word_def.json")
    print(word_def.find_definition("corner"))


if __name__ == '__main__':
    test()
