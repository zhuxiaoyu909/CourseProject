from typing import List, Set
import nltk
import string
import re
from contractions import Contractions

# nltk.download('punkt')
# nltk.download("averaged_perceptron_tagger")
#
# tag_score = {"CC": 5, "CD": 1, "DT": 1, "EX": 1, "FW": 100, "IN": 5, "JJ": 2, "JJR": 3,
# "JJS": 4, "LS": 100, "MD": 3, "NN": 1, "NNS": 1, "NNP": 1, "NNPS": 2, "PDT": 2, "POS": 1,
# "PRP": 1, "PRP$": 1, "RB": 3, "RBR": 3, "RBS": 4, "RP": 5, "TO": 4, "UH": 1, "VB": 1, "VBG": 1,
# "VBD": 1, "VBN": 1, "VBP": 1, "VBZ": 1, "WDT": 5, "WP": 5, "WRB": 5}


class Sentence(object):
    _translator = str.maketrans('', '', string.punctuation)
    _contractions = Contractions()

    def __init__(self, sentence):
        self.sentence = sentence
        self.transformed_words = self.create_transformed_words()
        self.word_set = self.create_word_set()

    def create_transformed_words(self) -> List[str]:
        s = self.sentence.lower()
        s = re.sub(r"\d*", "", s)  # remove numbers.
        s = Sentence._contractions.fix(s)
        s = " ".join(re.split('\W+', s))  # remove punctuations.
        # s = s.translate(Sentence._translator)
        words = nltk.word_tokenize(s)
        return words

    def create_word_set(self) -> Set[str]:
        s = self.sentence.lower()
        s = " ".join(re.split('\W+', s))
        words = nltk.word_tokenize(s)
        return set(words)

    def transformed_word_count(self) -> int:
        return len(self.transformed_words)

    def word_count(self) -> int:
        return len(self.words)

    def __str__(self):
        return self.sentence


class Sentences(object):
    def __init__(self, arr: List[Sentence]):
        self.arr = arr

    def __len__(self):
        return len(self.arr)

    def filter_by_word(self, word: str):
        word_lowered = str(word).lower()
        new_arr = [s for s in self.arr if word_lowered in s.word_set]
        return Sentences(new_arr)


def test():
    # file_path = f"data/CBTest/data/cbtest_NE_train.txt"
    # file = CBFile(file_path=file_path)
    # df = file.to_pandas()
    # sentences = Sentences([Sentence(s) for s in df["sentence"].tolist()])
    # sentences_with_awake = sentences.filter_by_word("awake")
    # print(len(sentences_with_awake))
    pass


if __name__ == '__main__':
    test()


#
# class SentenceWithWordDifficulty(object):
#     def __init__(self, sentence: Sentence, word_difficulty: list):
#         self.sentence = sentence
#         self.word_difficulty = word_difficulty
#         self.pos = nltk.pos_tag(sentence.words)
#
#     def difficulty(self):
#         word_ranks = np.array([w.rank for w in self.word_difficulty], dtype=np.float)
#         return np.mean(word_ranks)
#
#     def pos_difficulty(self):
#         pos_score = 0
#         for _, tag in self.pos:
#             pos_score += tag_score[tag]
#         return pos_score
#
#     def __len__(self):
#         return len(self.sentence)
#
#     def __str__(self):
#         return f"{self.sentence.sentence} - (difficulty: {self.difficulty()}, POS_difficulty: {self.pos_difficulty()}, words: {len(self)})"
#
#     def to_pandas_word_difficulty(self):
#         word_dict = {
#             "word":         [w.word for w in self.word_difficulty],
#             "rank":         [w.rank for w in self.word_difficulty],
#             "POS":          [p[1] for p in self.pos],
#             "POS_Score":    [tag_score[p[1]] for p in self.pos]
#         }
#         return pd.DataFrame(data=word_dict)
#
#     @staticmethod
#     def with_word_difficulty(sentence: Sentence, word_frequency: WordFrequencies):
#         word_difficulty = [word_frequency.frequency(w) for w in sentence.words]
#         return SentenceWithWordDifficulty(sentence=sentence, word_difficulty=word_difficulty)
#
#
# def test():
#     examples = [
#         "What do you really think about it?",
#         "I don’t care about your past.",
#         "What do you think about that issue?",
#         "He genuinely cares about me.",
#         "Do you have any information about the project?",
#         "Our house is worth about 150,000 dollars.",
#         "Don’t worry too much about unimportant things.",
#         "John's mother abandoned him in cold heart after he was born",
#     ]
#     word_frequencies = WordFrequencies.read_excel(file_path="data/wordFrequency.xlsx")
#     for sentence in examples:
#         sentence = Sentence(sentence)
#         sentence = SentenceWithWordDifficulty.with_word_difficulty(sentence, word_frequencies)
#         print(sentence)
#         print(sentence.to_pandas_word_difficulty())
#         print()
#
#
# if __name__ == '__main__':
#     test()

