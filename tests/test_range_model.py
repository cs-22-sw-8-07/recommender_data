import os
from unittest import TestCase
from config import load_config
from quack_location_type import QuackLocationType
from range_model.range_model import RangeModel
from range_model.track_data import TrackData


class TestRangeModel(TestCase):
    def setUp(self):
        self._tests_folder = os.path.dirname(os.path.abspath(__file__))
        self._config = load_config("test_config.cnf")

        track_data = TrackData()
        path = os.path.join(self._tests_folder, "test_resources", "test_CompleteIndividualTrackData.csv")
        track_data.load_csv(path)

        self.range_model = RangeModel(self._config, track_data)
        path = os.path.join(self._tests_folder, "test_resources", "test_range_tracks.csv")
        self.range_model.load_track_csv(path)

    def test_correct_ranges__church_danceability(self):
        expected_result_bottom = 0.44
        expected_result_top = 0.49

        actual_bottom = self.range_model._bottom_range["church"][0]
        actual_top = self.range_model._top_range["church"][0]

        self.assertAlmostEqual(expected_result_bottom, actual_bottom, places=5)
        self.assertAlmostEqual(expected_result_top, actual_top, places=5)

    def test_correct_ranges__church_energy(self):
        expected_result_bottom = 0.24
        expected_result_top = 0.34

        actual_bottom = self.range_model._bottom_range["church"][1]
        actual_top = self.range_model._top_range["church"][1]

        self.assertAlmostEqual(expected_result_bottom, actual_bottom, places=5)
        self.assertAlmostEqual(expected_result_top, actual_top, places=5)

    def test_correct_range_priority__church(self):
        expected_priorities = [True, True, False, False, False, False, False, False, False]

        actual_priorities = self.range_model._attribute_priority["church"]

        self.assertEqual(expected_priorities, actual_priorities)

    def test_correct_range_priority__beach(self):
        expected_priorities = [False, False, False, True, True, False, False, False, False]

        actual_priorities = self.range_model._attribute_priority["beach"]

        self.assertEqual(expected_priorities, actual_priorities)

    def test_get_tracks__church(self):
        expected_track_names = ["Church Song 6", "Church Song 5", "Church Song 7", "Church Song 8"]

        tracks = self.range_model.get_tracks(QuackLocationType.church)
        actual_track_names = [track.name for track in tracks]

        self.assertEqual(expected_track_names, actual_track_names)

    def test_get_tracks__church_amount(self):
        expected_tracks = 2

        tracks = self.range_model.get_tracks(QuackLocationType.church, amount=2)
        actual_tracks = len(tracks)

        self.assertEqual(expected_tracks, actual_tracks)

    def test_get_tracks__church_amount_offset(self):
        expected_track_names = ["Church Song 7", "Church Song 8"]

        tracks = self.range_model.get_tracks(QuackLocationType.church, amount=2, offset=2)
        actual_track_names = [track.name for track in tracks]

        self.assertEqual(expected_track_names, actual_track_names)
