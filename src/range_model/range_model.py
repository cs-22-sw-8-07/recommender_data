import numpy as np
from configparser import ConfigParser
from track import load_track_csv
from quack_location_type import QuackLocationType
from range_model.track_data import TrackData


class RangeModel:
    def __init__(self, config: ConfigParser, track_data: TrackData):
        self._slice_pct = config.getfloat('RANGE_MODEL', 'slice_percentage')
        self._no_of_range_attributes = config.getint('RANGE_MODEL', 'no_of_range_attributes')
        self._track_data = track_data
        self._bottom_range = {}
        self._top_range = {}
        self._average = {}
        self._attribute_priority = {}
        self._tracks = []
        self._data = None

        self._create_ranges()

    def _create_ranges(self):
        self._bottom_range = {}
        self._top_range = {}
        self._average = {}
        self._attribute_priority = {}
        difference = {}
        size_of_vecs = self._track_data.size_of_vecs()

        for key in self._track_data.keys():
            self._bottom_range[key] = [0 for _ in range(0, size_of_vecs)]
            self._top_range[key] = [1 for _ in range(0, size_of_vecs)]
            self._average[key] = [0.5 for _ in range(0, size_of_vecs)]
            difference[key] = [0 for _ in range(0, size_of_vecs)]
            for i in range(0, size_of_vecs):
                sorted_vars = sorted(self._track_data[key], key=lambda v: v[i])
                self._bottom_range[key][i] = sorted_vars[int(self._track_data.tracks_in_key(key) * self._slice_pct)][i]
                self._top_range[key][i] = sorted_vars[int(self._track_data.tracks_in_key(key) * (1.0 - self._slice_pct)) - 1][i]
                self._average[key][i] = sum([vec[i] for vec in self._track_data[key]])/len(self._track_data[key])
                difference[key][i] = self._top_range[key][i] - self._bottom_range[key][i]

        for key in self._track_data.keys():
            self._attribute_priority[key] = [False for _ in range(0, size_of_vecs)]
            sorted_diff = sorted(difference[key])
            for i in range(0, self._no_of_range_attributes):
                self._attribute_priority[key][difference[key].index(sorted_diff[i])] = True

    def load_track_csv(self, csv_path: str):
        self._data, self._tracks = load_track_csv(csv_path)
        for track in self._tracks:
            self._track_data.normalize_vec(track.attribute_vec)

    def _range_filter(self, vec, bottom, top):
        for i in range(0, len(bottom)):
            if vec[i] < bottom[i] or vec[i] > top[i]:
                return False
        return True

    def _range_sort_euclidian_distance(self, vec, key: str):
        vec_compare = []
        avg_compare = []

        for i in range(0, len(vec)):
            if not self._attribute_priority[key][i]:
                continue

            vec_compare.append(vec[i])
            avg_compare.append(self._average[key][i])

        return np.linalg.norm(np.array([vec_compare]) - np.array([avg_compare]))

    def get_tracks(self, location_type: QuackLocationType, amount: int = 1000, offset: int = 0):
        key = location_type.name

        filter_bottom = [-9999.0 for _ in range(0, self._track_data.size_of_vecs())]
        filter_top = [9999.0 for _ in range(0, self._track_data.size_of_vecs())]

        for i in range(0, len(self._track_data.keys())):
            if not self._attribute_priority[key][i]:
                continue

            filter_bottom[i] = self._bottom_range[key][i]
            filter_top[i] = self._top_range[key][i]

        filtered = list(filter(lambda track: self._range_filter(track.attribute_vec, filter_bottom, filter_top), self._tracks))
        tracks = list(sorted(filtered, key=lambda track: self._range_sort_euclidian_distance(track.attribute_vec, key)))[offset:offset+amount]
        return tracks
