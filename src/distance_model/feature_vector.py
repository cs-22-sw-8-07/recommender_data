import pandas


class FeatureVector:
    def __init__(self):
        self._data = None
        self._dict = {}

    def load_feature_vectors(self, path: str):
        self._data = pandas.read_csv(path)
        self._dict = {}
        for v in self._data.values:
            self._dict[v[0]] = v[1:len(v)]

    def __getitem__(self, item):
        return self._dict[item]
