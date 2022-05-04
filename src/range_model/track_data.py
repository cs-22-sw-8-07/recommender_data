import pandas


class TrackData:
    def __init__(self):
        self._dict = {}
        self._min_vec = []
        self._max_vec = []

    def __getitem__(self, item):
        return self._dict[item]

    def load_csv(self, path: str):
        self._dict = {}
        data = pandas.read_csv(path)
        for v in data.values:
            # Adds the key in column 2 if dict does not already contain it
            if v[1] not in self._dict.keys():
                self._dict[v[1]] = []

            # Reads the track data using only the given columns
            new_vec = [v[5], v[6], v[8]]
            new_vec.extend(v[10:16])

            self._dict[v[1]].append(new_vec)

        self._normalize()

    def keys(self):
        # Returns a list of all location types
        return list(self._dict.keys())

    def tracks_in_key(self, key: str):
        # Returns the number of tracks in a given location
        return len(self._dict[key])

    def size_of_vecs(self) -> int:
        # Returns the number of attributes per track
        return len(list(self._dict.values())[0][0])

    def normalize_vec(self, attribute_vec: list):
        # Normalizes just one of the track vectors
        for i in range(0, len(attribute_vec)):
            if abs(self._max_vec[i]) == abs(self._min_vec[i]):
                # Prevents division by 0
                continue
            # Normalize for each attribute
            attribute_vec[i] = (attribute_vec[i] - self._min_vec[i])/(self._max_vec[i] - self._min_vec[i])

    def _normalize(self):
        # Normalizes each column to be the values between 0 and 1
        size_of_vecs = self.size_of_vecs()
        track_values = self._vectors()

        # Finds the minimum and maximum values for each attribute
        # Saves the min vec and max vec to enable normalizing vectors that does not originate in the track dataset with the same factors
        self._min_vec = [9999.0 for _ in range(0, size_of_vecs)]
        self._max_vec = [-9999.0 for _ in range(0, size_of_vecs)]
        for i in range(0, len(track_values)):
            for j in range(0, size_of_vecs):
                if self._min_vec[j] > track_values[i][j]:
                    self._min_vec[j] = track_values[i][j]
                if self._max_vec[j] < track_values[i][j]:
                    self._max_vec[j] = track_values[i][j]

        # Uses the min vec and max vec to normalize each column
        for key in self._dict.keys():
            for i in range(0, len(self._dict[key])):
                self.normalize_vec(self._dict[key][i])

    def _vectors(self):
        # Returns each vector of each location type
        # (Flattens a structure [[1, 2], [3, 4]] -> [1, 2, 3, 4])
        return [val for values in self._dict.values() for val in values]

