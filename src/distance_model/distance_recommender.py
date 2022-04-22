import os

import pandas as pd

import quack_location_type
from distance_model.feature_vector import FeatureVector
from distance_model.vector_space_model import VectorSpaceModel
from quack_location_type import QuackLocationType


class DistanceRecommender:
    def __init__(self, feature_vec: FeatureVector, vsm: VectorSpaceModel):
        self._feature_vec = feature_vec
        self._vsm = vsm

    def get_playlist(self, location: QuackLocationType):
        key = location.name
        result = {"id": [], "name": [], "artist": []}

        tracks = self._vsm.closest_tracks(self._feature_vec[key])

        for track in tracks:
            artist_list = []
            for artist in track.artists:
                artist_list.append(artist)
            artists = ", ".join(artist_list)

            result["id"].append(track.id)
            result["name"].append(track.name)
            result["artist"].append(artists)

        dataframe = pd.DataFrame.from_dict(result)

        dataframe.to_csv(
            os.path.join("distance_recommender_tracks", quack_location_type.QuackLocationType(location).name +
                         "_tracks.csv"),
            sep=",", header=False, index=False)
        return

