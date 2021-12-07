import pandas as pd


class WordFrequency(object):
    def __init__(self, word, rank):
        self.word = word
        self.rank = rank

    def __str__(self):
        return f"word: {self.word}, rank: {self.rank}"


class WordFrequencies(object):
    def __init__(self, mappings):
        self.mappings = mappings
        self.max_rank = 6000

    def frequency(self, word):
        if word in self.mappings:
            return self.mappings[word]
        else:
            return WordFrequency(word=word, rank=self.max_rank)

    def __len__(self):
        return len(self.mappings)

    @classmethod
    def read_excel(cls, file_path):
        df = pd.read_excel(io=open(file_path, 'rb'), sheet_name='4 forms (219k)', engine="openpyxl")
        mappings = {}
        for i, row in df.iterrows():
            rank = row['rank']
            word = row['word']
            if word not in mappings:
                mappings[word] = WordFrequency(word=word, rank=rank)
        return WordFrequencies(mappings=mappings)


def test():
    word_frequencies = WordFrequencies.read_excel(file_path="data/wordFrequency.xlsx")
    print(f"total words: {len(word_frequencies)}")
    examples = ["you", "say", "what", "because", "something", "through"]
    for word in examples:
        feq = word_frequencies.frequency(word=word)
        print(feq)


if __name__ == '__main__':
    test()
