import os

import pandas as pd

import quack_location_type
from quack_location_type import QuackLocationType
from service_response import Errors, service_response_error_json
from range_model.range_model import RangeModel


class RangeRecommender:
    def __init__(self, range_model: RangeModel):
        self._range_model = range_model

    def get_playlist(self, location: QuackLocationType):
        error_no = 0
        result = {"id": [], "name": [], "artist": []}

        try:
            error_no = Errors.CouldNotFindTracksFromRangeRecommender
            # TODO: tracks missing album cover info
            tracks = self._range_model.get_tracks(location)
            for track in tracks:
                artist_list = []
                # TODO ['artist 1','artist 2']
                for artist in track.artists:
                    artist_list.append(artist)
                artists = ", ".join(artist_list)

                result["id"].append(track.id)
                result["name"].append(track.name)
                result["artist"].append(artists)

            dataframe = pd.DataFrame.from_dict(result)

            error_no = Errors.CouldNotCreateCSVFile
            dataframe.to_csv(
                os.path.join("range_recommender_tracks", quack_location_type.QuackLocationType(location).name +
                             "_tracks.csv"),
                sep=",", header=False, index=False)
        except:
            return service_response_error_json(error_no.value)

        return
