from difficulty_ranker import DifficultyRanker, SentenceDifficulty
from sentence import Sentence
import nltk
from typing import List, Dict
import json


class POSDifficulty(SentenceDifficulty):
    def __init__(
            self,
            sentence: Sentence,
            tag_score: Dict[str, int],
            max_value: float,
            max_difficulty_value: float):
        super().__init__()

        self.tag_score = tag_score
        self.pos = nltk.pos_tag(sentence.transformed_words)
        self.max_value = max_value
        self.max_difficulty_value = max_difficulty_value
        self.unit_difficulty = max_value/max_difficulty_value

    def difficulty_value(self) -> float:
        raw_value = self.difficulty_raw_value()
        value = min(raw_value/self.unit_difficulty, self.max_value)
        return self.round(value)

    def difficulty_raw_value(self):
        pos_score = 0.0
        for _, tag in self.pos:
            pos_score += self.tag_score[tag]
        return self.round(pos_score)

    def to_dict(self) -> Dict[str, List]:
        return {
            "POS":          [p[1] for p in self.pos],
            "POS_Score":    [self.tag_score[p[1]] for p in self.pos]
        }

    def to_compact_dict(self) -> Dict[str, str]:
        desc = [f"{p[0]}({p[1]}:{self.tag_score[p[1]]})" for p in self.pos]
        return {
            "POS Difficulty": self.difficulty_value(),
            "POS Raw Difficulty": self.difficulty_raw_value(),
            "POS Difficulty Details": ", ".join(desc)
        }


class POSDifficultyRanker(DifficultyRanker):
    def __init__(self):
        nltk.download("averaged_perceptron_tagger")
        # self.tag_score = {
        #     "CC": 5, "CD": 1, "DT": 1, "EX": 1, "FW": 100, "IN": 5, "JJ": 2, "JJR": 3,
        #      "JJS": 4, "LS": 100, "MD": 3, "NN": 1, "NNS": 1, "NNP": 1, "NNPS": 2, "PDT": 2, "POS": 1,
        #      "PRP": 1, "PRP$": 1, "RB": 3, "RBR": 3, "RBS": 4, "RP": 5, "TO": 4, "UH": 1, "VB": 1, "VBG": 1,
        #      "VBD": 1, "VBN": 1, "VBP": 1, "VBZ": 1, "WDT": 5, "WP": 5, "WRB": 5
        # }
        with open('data/pos_difficulty.json', 'r') as myfile:
            data = myfile.read()
        self.tag_score = json.loads(data)

    def rank(self, sentence: Sentence) -> SentenceDifficulty:
        return POSDifficulty(sentence=sentence, tag_score=self.tag_score, max_value=60, max_difficulty_value=4.0)


def test():
    examples = [
        "What do you really think about it?",
        "I don’t care about your past.",
        "What do you think about that issue?",
        "He genuinely cares about me.",
        "Do you have any information about the project?",
        "Our house is worth about 150,000 dollars.",
        "Don’t worry too much about unimportant things.",
        "John's mother abandoned him in cold heart after he was born",
    ]

    ranker = POSDifficultyRanker()
    for sentence in examples:
        sentence = Sentence(sentence)
        difficulty = ranker.rank(sentence)
        print(str(sentence))
        print(difficulty.to_dict())
        print()


if __name__ == '__main__':
    test()
