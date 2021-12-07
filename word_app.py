from index import Index
from sentence_ranker import SentenceRanker, RankedSentences
from word_frequency import WordFrequencies
from word_difficulty_ranker import WordDifficultyRanker
from pos_difficulty_ranker import POSDifficultyRanker
from difficulty_ranker import DifficultyRankers
from word_definition import WordDefinitions
from word_result import WordResult


class WordApp(object):
    def __init__(
            self,
            idx: Index,
            ranker: SentenceRanker,
            definitions: WordDefinitions
    ):
        self.idx = idx
        self.ranker = ranker
        self.definitions = definitions

    def search(self, word: str, n_results: int = 10) -> WordResult:
        ranked_sentences = self.search_for_sentences(word=word)
        ranked_sentences.sort_by_difficulty()
        definition = self.definitions.find_definition(word)
        return WordResult(word=word, definition=definition, ranked_sentences=ranked_sentences.sentences[:n_results])

    def search_for_sentences(self, word: str) -> RankedSentences:
        sentences = self.idx.search(query_text=word)
        return self.ranker.rank(sentences)


def create_app() -> WordApp:
    idx = Index(config_file_path="config.toml")
    word_frequencies = WordFrequencies.read_excel(file_path="data/wordFrequency.xlsx")

    word_difficulty_ranker = WordDifficultyRanker(word_frequencies=word_frequencies)
    pos_difficulty_ranker = POSDifficultyRanker()
    difficulty_rankers = DifficultyRankers(
        rankers=[word_difficulty_ranker, pos_difficulty_ranker],
        weights=[0.5, 0.5])
    ranker = SentenceRanker(difficulty_ranker=difficulty_rankers)

    word_def = WordDefinitions(json_file_path="data/word_def.json")

    app = WordApp(idx=idx, ranker=ranker, definitions=word_def)
    return app


def test():
    app = create_app()
    word_result = app.search(word="corner")
    print(word_result.to_html())


if __name__ == '__main__':
    test()
