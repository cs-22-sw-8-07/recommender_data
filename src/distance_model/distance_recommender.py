import os

import pandas as pd

import quack_location_type
from distance_model.feature_vector import FeatureVector
from distance_model.vector_space_model import VectorSpaceModel
from quack_location_type import QuackLocationType
from service_response import Errors, service_response_error_json


class DistanceRecommender:
    def __init__(self, feature_vec: FeatureVector, vsm: VectorSpaceModel):
        self._feature_vec = feature_vec
        self._vsm = vsm

    def get_playlist(self, location: QuackLocationType):
        key = location.name
        error_no = 0
        result = {"id": [], "name": [], "artist": []}

        try:
            error_no = Errors.CouldNotFindClosestTracks
            # TODO: tracks missing album cover info
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

            error_no = Errors.CouldNotCreateCSVFile
            dataframe.to_csv(
                os.path.join("distance_recommender_tracks", quack_location_type.QuackLocationType(location).name +
                             "_tracks.csv"),
                sep=",", header=False, index=False)
        except:
            return service_response_error_json(error_no.value)

        return

