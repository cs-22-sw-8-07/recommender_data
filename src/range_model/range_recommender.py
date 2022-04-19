import os

import pandas as pd

import quack_location_type
from quack_location_type import QuackLocationType
from recommender import Recommender
from service_response import Errors, service_response_error_json
from range_model.range_model import RangeModel


class RangeRecommender(Recommender):
    def __init__(self, range_model: RangeModel):
        super().__init__()
        self._range_model = range_model

    def get_playlist(self, location: QuackLocationType):
        error_no = 0
        result = []

        try:
            error_no = Errors.CouldNotFindTracksFromRangeRecommender
            tracks = self._range_model.get_tracks(location)
            for track in tracks:
                result.append(track.id)

            error_no = Errors.CouldNotCreateCSVFile
            pd.DataFrame(result).to_csv(
                os.path.join("range_recommender_tracks", quack_location_type.QuackLocationType(location).name +
                             "_tracks.csv"),
                sep=",", header=False)
            return
        except:
            return service_response_error_json(error_no.value)
