import pandas as pd


class CBFile(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_lines(self) -> []:
        lines = []
        with open(self.file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line != "":
                    lines.append(line)
        return lines

    def to_pandas(self) -> pd.DataFrame:
        lines = self.read_lines()
        list_of_tuples = []
        for line in lines:
            num, content = line.split(" ", 1)
            list_of_tuples.append((int(num), content))
        return pd.DataFrame(list_of_tuples, columns=["number", "sentence"])


def test():
    file_path = "data/CBTest/data/cbtest_CN_train.txt"
    cbfile = CBFile(file_path)
    print(cbfile.read_lines()[:2])
    print(cbfile.to_pandas())


if __name__ == '__main__':
    test()
