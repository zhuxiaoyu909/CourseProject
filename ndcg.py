from typing import List

import numpy as np
import pandas as pd
from word_app import create_app


class NDCG(object):
    def __init__(self, eval_queries_file_path):
        self.queries_df = pd.read_csv(eval_queries_file_path)

    def score(self, word: str, sentences: List[str]):
        reference_df = self.queries_df[self.queries_df["word"] == word].sort_values(by="gain", ascending=False)
        actual_df = pd.DataFrame({
            "sentence": sentences
        })
        merged_df = actual_df.merge(reference_df, on='sentence', how='left')
        actual_gains = merged_df["gain"].to_numpy()
        actual_gains = actual_gains[~np.isnan(actual_gains)]
        actual_total_gain = NDCG.total_gain(actual_gains)
        ideal_total_gain = NDCG.total_gain(reference_df["gain"].to_numpy())
        return actual_total_gain/ideal_total_gain

    @staticmethod
    def total_gain(gains):
        return np.sum(gains/np.log2(np.arange(start=2, stop=len(gains)+2)))


def test():
    app = create_app()
    word = "spirit"
    word_result = app.search(word, n_results=5)
    sentences = [str(s) for s in word_result.ranked_sentences]
    print("\n".join(sentences))

    ndcg = NDCG("data/eval_queries.csv")
    print(ndcg.score(word, sentences))


if __name__ == '__main__':
    test()
