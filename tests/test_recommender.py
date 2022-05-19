import json
import os
import uuid
from unittest import TestCase
from quack_location_type import QuackLocationType
from recommender import Recommender
from track import load_track_csv


class TestRecommender(TestCase):
    recommender = None

    def setUp(self):
        self._tests_folder = os.path.dirname(os.path.abspath(__file__))
        self.recommender = Recommender()

    def test_get_playlist_json__valid_id(self):
        path = os.path.join(self._tests_folder, "test_resources", "test_distance_tracks.csv")
        _, tracks = load_track_csv(path)

        result_str = self.recommender._get_playlist_json(tracks, QuackLocationType.church)
        result_json = json.loads(result_str)
        result_id = result_json["result"]["id"]

        try:
            uuid.UUID(result_id)
        except:
            self.fail()
