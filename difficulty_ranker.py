import abc
from sentence import Sentence
import pandas as pd
from typing import Dict, List


class SentenceDifficulty(object):
    def __init__(self):
        self.ndigits = 2

    @abc.abstractmethod
    def difficulty_value(self) -> float:
        raise NotImplementedError

    def round(self, value):
        return round(value, ndigits=self.ndigits)

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, List]:
        raise NotImplementedError

    @abc.abstractmethod
    def to_compact_dict(self) -> Dict[str, str]:
        raise NotImplementedError


class SentenceDifficulties(SentenceDifficulty):
    def __init__(self, difficulties: [], weights: []):
        super().__init__()

        assert len(difficulties) == len(weights)

        self.difficulties = difficulties
        self.weights = weights

    def difficulty_value(self) -> float:
        total = 0.0
        for d, w in zip(self.difficulties, self.weights):
            total += w * d.difficulty_value()
        return self.round(total)

    def to_dict(self) -> Dict[str, List]:
        merged = {}
        for d in self.difficulties:
            new_dict = d.to_dict()
            merged = {**merged, **new_dict}
        return merged

    def to_compact_dict(self) -> Dict[str, str]:
        calc = [f"{d.difficulty_value()}*{w}" for d, w in zip(self.difficulties, self.weights)]
        merged = {
            "Overall Difficulty": self.difficulty_value(),
            "Overall Difficulty Calculation": " + ".join(calc)
        }
        for d in self.difficulties:
            new_dict = d.to_compact_dict()
            merged = {**merged, **new_dict}
        return merged

    def __str__(self):
        desc = [f"difficulty: {str(d)}, weight: {w}" for d, w in zip(self.difficulties, self.weights)]
        return "\n".join(desc)

    def to_pandas(self):
        return pd.DataFrame(data=self.to_dict())


class DifficultyRanker(object):
    @abc.abstractmethod
    def rank(self, sentence: Sentence) -> SentenceDifficulty:
        raise NotImplementedError


class DifficultyRankers(DifficultyRanker):
    def __init__(self, rankers: [], weights: []):
        assert len(rankers) == len(weights)

        self.rankers = rankers
        self.weights = weights

    def rank(self, sentence: Sentence) -> SentenceDifficulty:
        difficulties = []
        for ranker in self.rankers:
            difficulty = ranker.rank(sentence)
            difficulties.append(difficulty)
        return SentenceDifficulties(difficulties=difficulties, weights=self.weights)
