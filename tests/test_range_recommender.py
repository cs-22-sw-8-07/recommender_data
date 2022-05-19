import json
import os
from unittest import TestCase
from config import load_config
from quack_location_type import QuackLocationType
from range_model.range_model import RangeModel
from range_model.range_recommender import RangeRecommender
from range_model.track_data import TrackData


class TestRangeRecommender(TestCase):
    recommender = None

    def setUp(self):
        self._tests_folder = os.path.dirname(os.path.abspath(__file__))
        self._config = load_config("test_config.cnf")

        track_data = TrackData()
        path = os.path.join(self._tests_folder, "test_resources", "test_CompleteIndividualTrackData.csv")
        track_data.load_csv(path)

        range_model = RangeModel(self._config, track_data)
        path = os.path.join(self._tests_folder, "test_resources", "test_range_tracks.csv")
        range_model.load_track_csv(path)

        self.recommender = RangeRecommender(range_model)

    def test_get_playlist__church(self):
        expected_result_str = """{"result": {"location_type": "church", "tracks": [{"id": "0BRXJHRNGQ3W4v9frnSfhu", "name": "Church Song 6", "artist": "Artist 6", "image": "none"}, {"id": "08y9GfoqCWfOGsKdwojr5e", "name": "Church Song 5", "artist": "Artist 5", "image": "none"}, {"id": "0Dd9ImXtAtGwsmsAD69KZT", "name": "Church Song 7", "artist": "Artist 7", "image": "none"}, {"id": "0IA0Hju8CAgYfV1hwhidBH", "name": "Church Song 8", "artist": "Artist 8", "image": "none"}]}, "is_successful": 1, "error_no": 0}"""
        expected_result_json = json.loads(expected_result_str)

        result_str = self.recommender.get_playlist(QuackLocationType.church)
        result_json = json.loads(result_str)
        result_json["result"].pop("id")

        self.assertEqual(result_json, expected_result_json)
