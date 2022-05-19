import os

import pandas as pd

import quack_location_type
from playlists_gen import Data_gen
from quack_location_type import QuackLocationType
from range_model.range_model import RangeModel


class RangeRecommender:
    def __init__(self, range_model: RangeModel):
        self._range_model = range_model

    def get_playlist(self, location: QuackLocationType, token: str, base_folder):
        result = {"id": [], "name": [], "artist": [], "image": []}
        sp = Data_gen(token)

        tracks = self._range_model.get_tracks(location)
        for track in tracks:
            image = sp.get_track_image(track.id)

            artist_list = []
            for artist in track.artists:
                artist_list.append(artist)
            artists = ";".join(artist_list)

            result["id"].append(track.id)
            result["name"].append(track.name)
            result["artist"].append(artists)
            result["image"].append(image)

        dataframe = pd.DataFrame.from_dict(result)
        dataframe.to_csv(
            os.path.join(base_folder, "range_recommender_tracks", quack_location_type.QuackLocationType(location).name +
                         "_tracks.csv"),
            sep=",", header=False, index=False)
        return
