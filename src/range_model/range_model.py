import numpy as np
from configparser import ConfigParser
from track import load_track_csv
from quack_location_type import QuackLocationType
from track_data import TrackData


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

        for location in self._track_data.keys():
            # Initializes each dictionary with location keys and vectors for values.
            # The length of each vector is = number of attributes
            self._bottom_range[location] = [0 for _ in range(0, size_of_vecs)]
            self._top_range[location] = [1 for _ in range(0, size_of_vecs)]
            self._average[location] = [0.5 for _ in range(0, size_of_vecs)]
            difference[location] = [0 for _ in range(0, size_of_vecs)]
            for i in range(0, size_of_vecs):
                # Sorts the tracks in a key by attribute "i" from lowest to highest
                sorted_tracks = sorted(self._track_data[location], key=lambda v: v[i])
                # Finds the bottom range by finding the value in the sorted attributes with the required index from the bottom
                self._bottom_range[location][i] = sorted_tracks[int(self._track_data.tracks_in_key(location) * self._slice_pct)][i]
                # Finds the top range by finding the value in the sorted attributes with the required index from the top
                self._top_range[location][i] = sorted_tracks[int(self._track_data.tracks_in_key(location) * (1.0 - self._slice_pct)) - 1][i]
                # Finds the average by summarizing the column and dividing the number of tracks in this location
                self._average[location][i] = sum([vec[i] for vec in self._track_data[location]])/len(self._track_data[location])
                # Finds the difference between the top and the bottom range for the attribute
                difference[location][i] = self._top_range[location][i] - self._bottom_range[location][i]

        for location in self._track_data.keys():
            # For each location, initialize the attribute priority as lists of only "False" values
            self._attribute_priority[location] = [False for _ in range(0, size_of_vecs)]
            # Sort the difference list for the location from lowest to highest
            sorted_diff = sorted(difference[location])
            for i in range(0, self._no_of_range_attributes):
                # Find the first X values for the differences, and find their index.
                # Then set the attribute priority to true for the attribute index of the unsorted difference location list
                self._attribute_priority[location][difference[location].index(sorted_diff[i])] = True

    def load_track_csv(self, csv_path: str):
        # Loads the track dataset
        self._data, self._tracks = load_track_csv(csv_path)
        for track in self._tracks:
            # Normalize each track with the same factors that track_data normalized with
            self._track_data.normalize_vec(track.attribute_vec)

    def _range_filter(self, vec, bottom, top):
        # Returns False if the vector is filtered away with the given bottom and top range, otherwise True
        for i in range(0, len(bottom)):
            if vec[i] < bottom[i] or vec[i] > top[i]:
                return False
        return True

    def _range_sort_euclidian_distance(self, vec, key: str):
        # Compares a vector with the average vector of the given location key.
        vec_compare = []
        avg_compare = []

        for i in range(0, len(vec)):
            if not self._attribute_priority[key][i]:
                # If the index is not a priority attribute, skip
                continue

            vec_compare.append(vec[i])
            avg_compare.append(self._average[key][i])

        # Use linear algebra to compare the two vectors
        return np.linalg.norm(np.array([vec_compare]) - np.array([avg_compare]))

    def get_tracks(self, location_type: QuackLocationType, amount: int = 1000, offset: int = 0):
        # Get the tracks that is within the range filter, and closest to the average vector
        key = location_type.name

        # Intialize the filter as being so lenient that it does not filter away and songs
        filter_bottom = [-9999.0 for _ in range(0, self._track_data.size_of_vecs())]
        filter_top = [9999.0 for _ in range(0, self._track_data.size_of_vecs())]

        for i in range(0, len(self._track_data.keys())):
            # For each important attribute, change the filter to be the range
            if not self._attribute_priority[key][i]:
                # Each unimportant priority is skipped
                continue

            filter_bottom[i] = self._bottom_range[key][i]
            filter_top[i] = self._top_range[key][i]

        # The filtered view that contains only tracks inside the filter
        filtered = filter(lambda track: self._range_filter(track.attribute_vec, filter_bottom, filter_top), self._tracks)
        # The playlist that contains the tracks that are closest to the average vector of the location type.
        # Sliced to respect the offset and the amount of tracks in the parameters
        tracks = list(sorted(filtered, key=lambda track: self._range_sort_euclidian_distance(track.attribute_vec, key)))[offset:offset+amount]
        return tracks
