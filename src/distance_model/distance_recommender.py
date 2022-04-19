from distance_model.feature_vector import FeatureVector
from distance_model.vector_space_model import VectorSpaceModel
from quack_location_type import QuackLocationType
from recommender import Recommender
from service_response import Errors, service_response_error_json


class DistanceRecommender(Recommender):
    def __init__(self, feature_vec: FeatureVector, vsm: VectorSpaceModel):
        super().__init__()
        self._feature_vec = feature_vec
        self._vsm = vsm

    def get_playlist(self, location: QuackLocationType):
        key = location.name
        error_no = 0

        try:
            error_no = Errors.CouldNotFindClosestTracks
            return self._vsm.closest_tracks(self._feature_vec[key])
        except:
            return service_response_error_json(error_no.value)
