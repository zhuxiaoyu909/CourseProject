import metapy


class DummyRanker(metapy.index.RankingFunction):
    def __init__(self):
        super(DummyRanker, self).__init__()

    def score_one(self, sd):
        return 1.0


class Index(object):
    def __init__(self, config_file_path):
        self.idx = metapy.index.make_inverted_index(config_file_path)
        self.dummy_ranker = DummyRanker()

    def search(self, query_text: str):
        query = metapy.index.Document()
        query.content(query_text)
        results = self.dummy_ranker.score(self.idx, query, 200)
        docs = []
        for num, (d_id, _) in enumerate(results):
            content = self.idx.metadata(d_id).get('content')
            docs.append(content)
        return docs


def test():
    idx = Index(config_file_path="config.toml")
    results = idx.search(query_text="washed", n_results=100)
    print("\n".join(results[:10]))


if __name__ == '__main__':
    test()

# os.chdir('/Users/jiaxi/Documents/GitHub/CS410-Project/')
#
# documents_path = '/Users/jiaxi/Documents/GitHub/CS410-Project/data/cbtest_NE_train_test.txt'
# documents = []
#
#
# def build_documents(documents_path):
#     """
#     Read in the children's book data and cleanse it before building the index.
#     """
#     f = open(documents_path, 'r')
#     documents = f.readlines()
#     f.close()
#
#     documents = list(filter(lambda x: x != '\n', documents))  # remove empty lines
#     documents = list(filter(lambda x: x[0:2] != '21', documents))  # remove the 21st sentence as it's used as the query for training
#     documents = list(filter(lambda x: x.find('|') == -1, documents))  # remove lines with weird characters
#
#     for l in range(len(documents)): # remove the numbering at the beginning of each sentence
#         if documents[l][1].isdigit():
#             documents[l] = documents[l][3:]
#         else:
#             documents[l] = documents[l][2:]
#
#     documents = set(documents)  # remove duplicate sentences
#
#     with open('/Users/jiaxi/Documents/GitHub/CS410-Project/idx_data/idx_data.dat', 'w') as f:
#         for l in documents:
#             f.write(l)



