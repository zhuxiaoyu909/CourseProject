from difficulty_ranker import DifficultyRanker, SentenceDifficulty
from sentence import Sentence
import numpy as np
from word_frequency import WordFrequencies, WordFrequency
from typing import List, Dict


class WordDifficulty(SentenceDifficulty):
    def __init__(self, difficulties: List[WordFrequency], max_value: float, max_difficulty_value: float):
        super().__init__()
        self.difficulties = difficulties
        self.max_value = max_value
        self.max_difficulty_value = max_difficulty_value
        self.unit_difficulty = max_value/max_difficulty_value

    def difficulty_value(self):
        raw_value = self.difficulty_raw_value()
        value = min(raw_value/self.unit_difficulty, self.max_value)
        return self.round(value)

    def difficulty_raw_value(self):
        word_ranks = np.array([w.rank for w in self.difficulties], dtype=np.float)
        return self.round(np.mean(word_ranks))

    def to_dict(self) -> Dict[str, List]:
        return {
            "rank":  [w.rank for w in self.difficulties],
        }

    def to_compact_dict(self) -> Dict[str, str]:
        desc = ", ".join([f"{w.word}({w.rank})" for w in self.difficulties])
        return {
            "Word Difficulty": self.difficulty_value(),
            "Word Raw Difficulty": self.difficulty_raw_value(),
            "Word Difficulty Details": desc
        }


class WordDifficultyRanker(DifficultyRanker):
    def __init__(self, word_frequencies: WordFrequencies, max_difficulty_value: float = 4.0):
        self.word_frequencies = word_frequencies
        self.max_difficulty_value = max_difficulty_value

    def rank(self, sentence: Sentence) -> SentenceDifficulty:
        word_difficulties = [self.word_frequencies.frequency(w) for w in sentence.transformed_words]
        return WordDifficulty(
            difficulties=word_difficulties,
            max_value=self.word_frequencies.max_rank,
            max_difficulty_value=self.max_difficulty_value)
