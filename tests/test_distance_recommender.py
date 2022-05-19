import json
import os
from unittest import TestCase
from distance_model.distance_recommender import DistanceRecommender
from distance_model.feature_vector import FeatureVector
from distance_model.vector_space_model import VectorSpaceModel
from quack_location_type import QuackLocationType
from track import load_track_csv


class TestDistanceRecommender(TestCase):
    recommender = None

    def setUp(self):
        self._tests_folder = os.path.dirname(os.path.abspath(__file__))

        feature_vector = FeatureVector()
        path = os.path.join(self._tests_folder, "test_resources", "test_allLocationFeatureVector.csv")
        feature_vector.load_feature_vectors(path)

        vsm = VectorSpaceModel()
        path = os.path.join(self._tests_folder, "test_resources", "test_distance_tracks.csv")
        vsm.load_track_csv(path)

        self.recommender = DistanceRecommender(feature_vector, vsm)

    def test_get_playlist__church(self):
        expected_result_str = """{"result": {"location_type": "church", "tracks": [{"id": "35iwgR4jXetI318WEWsa1Q", "name": "Song 1", "artist": "Artist 1", "image": "none"}, {"id": "021ht4sdgPcrDgSk7JTbKY", "name": "Song 2", "artist": "Artist 2", "image": "none"}, {"id": "07A5yehtSnoedViJAZkNnc", "name": "Song 3", "artist": "Artist 3, Additional Artist", "image": "none"}, {"id": "08FmqUhxtyLTn6pAh6bk45", "name": "Song 4", "artist": "Artist 4", "image": "none"}, {"id": "08y9GfoqCWfOGsKdwojr5e", "name": "Song 5", "artist": "Artist 5", "image": "none"}, {"id": "0BRXJHRNGQ3W4v9frnSfhu", "name": "Song 6", "artist": "Artist 6", "image": "none"}, {"id": "0Dd9ImXtAtGwsmsAD69KZT", "name": "Song 7", "artist": "Artist 7", "image": "none"}, {"id": "0IA0Hju8CAgYfV1hwhidBH", "name": "Song 8", "artist": "Artist 8", "image": "none"}, {"id": "0IgI1UCz84pYeVetnl1lGP", "name": "Song 9", "artist": "Artist 9", "image": "none"}, {"id": "0JV4iqw2lSKJaHBQZ0e5zK", "name": "Song 10", "artist": "Artist 10", "image": "none"}]}, "is_successful": 1, "error_no": 0}"""
        expected_result_json = json.loads(expected_result_str)

        result_str = self.recommender.get_playlist(QuackLocationType.church)
        result_json = json.loads(result_str)
        result_json["result"].pop("id")

        self.assertEqual(result_json, expected_result_json)

    def test_get_playlist__beach_closest_first(self):
        expected_result_str = """{"result": {"location_type": "beach", "tracks": [{"id": "0l3BQsVJ7F76wlN5QhJzaP", "name": "Song 20", "artist": "Artist 20", "image": "none"}, {"id": "0kCB1bDVBC8gWCFcnJyIZc", "name": "Song 19", "artist": "Artist 19", "image": "none"}, {"id": "0grXU6GKVNCVMJbseA0Uhe", "name": "Song 18", "artist": "Artist 18", "image": "none"}, {"id": "0eb1PfHxT6HnXvvdUOzmME", "name": "Song 17", "artist": "Artist 17", "image": "none"}, {"id": "0cC9CYjLRIzwchQ42xVnq6", "name": "Song 16", "artist": "Artist 16", "image": "none"}, {"id": "0TWsNj5iSvbMTtbEDP7A4V", "name": "Song 15", "artist": "Artist 15", "image": "none"}, {"id": "0QiT0Oo5QdLXdFw6RDOj7h", "name": "Song 14", "artist": "Artist 14", "image": "none"}, {"id": "0PH9AACae1f957JAavhOl2", "name": "Song 13", "artist": "Artist 13", "image": "none"}, {"id": "0PE42H6tslQuyMMiGRiqtb", "name": "Song 12", "artist": "Artist 12", "image": "none"}, {"id": "0OYGe21oScKJfanLyM7daU", "name": "Song 11", "artist": "Artist 11", "image": "none"}]}, "is_successful": 1, "error_no": 0}"""
        expected_result_json = json.loads(expected_result_str)

        result_str = self.recommender.get_playlist(QuackLocationType.beach)
        result_json = json.loads(result_str)
        result_json["result"].pop("id")

        self.assertEqual(result_json, expected_result_json)

    def test_get_playlist_json__church(self):
        expected_result_str = """{"result": {"location_type": "church", "tracks": [{"id": "35iwgR4jXetI318WEWsa1Q", "name": "Song 1", "artist": "Artist 1", "image": "none"}, {"id": "021ht4sdgPcrDgSk7JTbKY", "name": "Song 2", "artist": "Artist 2", "image": "none"}, {"id": "07A5yehtSnoedViJAZkNnc", "name": "Song 3", "artist": "Artist 3, Additional Artist", "image": "none"}, {"id": "08FmqUhxtyLTn6pAh6bk45", "name": "Song 4", "artist": "Artist 4", "image": "none"}, {"id": "08y9GfoqCWfOGsKdwojr5e", "name": "Song 5", "artist": "Artist 5", "image": "none"}, {"id": "0BRXJHRNGQ3W4v9frnSfhu", "name": "Song 6", "artist": "Artist 6", "image": "none"}, {"id": "0Dd9ImXtAtGwsmsAD69KZT", "name": "Song 7", "artist": "Artist 7", "image": "none"}, {"id": "0IA0Hju8CAgYfV1hwhidBH", "name": "Song 8", "artist": "Artist 8", "image": "none"}, {"id": "0IgI1UCz84pYeVetnl1lGP", "name": "Song 9", "artist": "Artist 9", "image": "none"}, {"id": "0JV4iqw2lSKJaHBQZ0e5zK", "name": "Song 10", "artist": "Artist 10", "image": "none"}]}, "is_successful": 1, "error_no": 0}"""
        expected_result_json = json.loads(expected_result_str)
        path = os.path.join(self._tests_folder, "test_resources", "test_distance_tracks.csv")
        _, tracks = load_track_csv(path)

        result_str = self.recommender._get_playlist_json(tracks[0:10], QuackLocationType.church)
        result_json = json.loads(result_str)
        result_json["result"].pop("id")

        self.assertEqual(result_json, expected_result_json)
