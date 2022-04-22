import pandas
import numpy as np
from track import Track, load_track_csv


class VectorSpaceModel:
    def __init__(self):
        self._data: pandas.DataFrame = None
        self._tracks = []
        self._min_vec = []
        self._max_vec = []

    def load_track_csv(self, csv_path: str):
        self._data, self._tracks = load_track_csv(csv_path)
        values_in_vec = len(self._tracks[0].attribute_vec)

        # Normalize values in vectors
        self._min_vec = [9999.0 for _ in range(0, values_in_vec)]
        self._max_vec = [-9999.0 for _ in range(0, values_in_vec)]
        for i in range(0, len(self._tracks)):
            for j in range(0, len(self._tracks[i].attribute_vec)):
                if self._min_vec[j] > self._tracks[i].attribute_vec[j]:
                    self._min_vec[j] = self._tracks[i].attribute_vec[j]
                if self._max_vec[j] < self._tracks[i].attribute_vec[j]:
                    self._max_vec[j] = self._tracks[i].attribute_vec[j]

        for t in self._tracks:
            t.normalize_vec(self._min_vec, self._max_vec)

    def _compare_euclidian(self, track_1: Track, track_2: Track) -> float:
        return np.linalg.norm(track_1.as_np_vec() - track_2.as_np_vec())

    def closest_tracks(self, feature_vec: [], amount: int = 1000):
        track = Track()
        track.attribute_vec = feature_vec
        track.normalize_vec(self._min_vec, self._max_vec)
        sorted_tracks = sorted(self._tracks, key=lambda t: self._compare_euclidian(t, track))
        return sorted_tracks[0:amount]


