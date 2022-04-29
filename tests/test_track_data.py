import os
from unittest import TestCase
from config import load_config
from range_model.track_data import TrackData


class TestTrackData(TestCase):
    def setUp(self):
        self._tests_folder = os.path.dirname(os.path.abspath(__file__))
        self._config = load_config("test_config.cnf")

        self.track_data = TrackData()
        path = os.path.join(self._tests_folder, "test_resources", "test_CompleteIndividualTrackData.csv")
        self.track_data.load_csv(path)

    def test_correct_no_of_vecs__church(self):
        expected_length = 10

        actual_length = len(self.track_data["church"])

        self.assertEqual(expected_length, actual_length)

    def test_correct_no_of_vecs__beach(self):
        expected_length = 10

        actual_length = len(self.track_data["beach"])

        self.assertEqual(expected_length, actual_length)

    def test_correct_no_of_tracks_in_key__church(self):
        expected_tracks = 10

        actual_tracks = self.track_data.tracks_in_key("church")

        self.assertEqual(expected_tracks, actual_tracks)

    def test_correct_keys(self):
        expected_keys = ["church", "beach"]

        actual_keys = self.track_data.keys()

        self.assertEqual(expected_keys, actual_keys)

    def test_correct_size_of_vecs(self):
        expected_size_of_vecs = 9

        actual_size_of_vecs = self.track_data.size_of_vecs()

        self.assertEqual(expected_size_of_vecs, actual_size_of_vecs)

    def test_normalized__loudness(self):
        expected_result_min = 0.0
        expected_result_mid = 0.5
        expected_result_max = 1.0

        actual_min = self.track_data["church"][0][2]
        actual_mid = self.track_data["church"][5][2]
        actual_max = self.track_data["beach"][9][2]

        self.assertAlmostEqual(expected_result_min, actual_min, places=5)
        self.assertAlmostEqual(expected_result_mid, actual_mid, places=5)
        self.assertAlmostEqual(expected_result_max, actual_max, places=5)

    def test_normalized__instrumentalness(self):
        expected_result_min = 0.0
        expected_result_max = 1.0

        actual_min = self.track_data["church"][0][5]
        actual_max = self.track_data["beach"][9][5]

        self.assertAlmostEqual(expected_result_min, actual_min, places=5)
        self.assertAlmostEqual(expected_result_max, actual_max, places=5)
