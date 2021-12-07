from sentence import Sentence
from difficulty_ranker import DifficultyRanker
from difficulty_ranker import SentenceDifficulty
import pandas as pd
import enum
from typing import List


class RankedSentence(object):
    def __init__(self, sentence: Sentence, difficulty: SentenceDifficulty):
        self.sentence = sentence
        self.difficulty = difficulty

    def __str__(self):
        return str(self.sentence)

    def __len__(self):
        return len(self.sentence.transformed_words)

    def difficulty_value(self) -> float:
        return self.difficulty.difficulty_value()


class Inclusion(enum.Enum):
    Sentence = 1
    Sentence_WordCount = 2
    Sentence_OverallDifficulty = 3
    All = 4


class RankedSentences(object):
    def __init__(self, sentences: List[RankedSentence]):
        self.sentences = sentences

    def __str__(self):
        return "\n".join([str(s) for s in self.sentences])

    def __len__(self):
        return len(self.sentences)

    def not_empty(self):
        return len(self.sentences) > 0

    def to_pandas(self, inclusion: Inclusion = Inclusion.Sentence):
        if inclusion == Inclusion.Sentence:
            df = pd.DataFrame([str(s)for s in self.sentences], columns=['Sentence'])
            return df
        elif inclusion == Inclusion.Sentence_WordCount:
            data = [(str(s), len(s)) for s in self.sentences]
            df = pd.DataFrame(data, columns=['Sentence', 'Word Count'])
            return df
        elif inclusion == Inclusion.Sentence_OverallDifficulty:
            data = [(str(s), s.difficulty_value()) for s in self.sentences]
            df = pd.DataFrame(data, columns=['Sentence', 'Overall Difficulty'])
            return df
        else:
            data = []
            for s in self.sentences:
                dict1 = {
                    'Sentence': str(s),
                    'Word Count': len(s)
                }
                merged = {**dict1, **s.difficulty.to_compact_dict()}
                data.append(merged)
            df = pd.DataFrame(data)
            return df

    def sort_by_difficulty(self):
        def by_difficulty(s):
            return s.difficulty_value()
        self.sentences.sort(reverse=False, key=by_difficulty)


class SentenceRanker(object):
    def __init__(
            self,
            difficulty_ranker: DifficultyRanker
    ):
        self.difficulty_ranker = difficulty_ranker

    def rank(self, sentences: []) -> RankedSentences:
        result = []
        for s in sentences:
            sentence = Sentence(s)
            difficulty = self.difficulty_ranker.rank(sentence)
            ranked_sentence = RankedSentence(sentence=sentence, difficulty=difficulty)
            result.append(ranked_sentence)
        return RankedSentences(sentences=result)
