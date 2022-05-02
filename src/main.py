import configparser
from configparser import ConfigParser
from typing import Optional

import quack_location_type
from config import load_config
from tasks import Tasks
import os
import sys
from range_model.track_data import TrackData
from quack_location_type import QuackLocationType
from range_model.range_model import RangeModel
from distance_model.feature_vector import FeatureVector
from distance_model.vector_space_model import VectorSpaceModel
from distance_model.distance_recommender import DistanceRecommender
from range_model.range_recommender import RangeRecommender


def main(argv):

    error_no = 0
    base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    token: str = argv[0]


    match argv[1]:
        case "dataset":
            TaskMaster = Tasks(token)
            # generates the track frequencies csv files.
            TaskMaster.task1_trackFrequencies()

            # generates the completed feature vectors and the invidual song meta data csv files.
            TaskMaster.task2_featureVectorsAndIndividualTracks()
        case "distance":
            config = load_config("config.cnf")

            feature_vec = FeatureVector()
            path = os.path.join(base_folder, "featureVectors", "allLocationFeatureVector.csv")
            feature_vec.load_feature_vectors(path)

            vsm = VectorSpaceModel()
            vsm.load_track_csv(config.get('RECOMMENDER', 'dataset_csv'))

            rec = DistanceRecommender(feature_vec, vsm)

            # For loop that generates the csv files. we could use QuackLocationType instead of numbers,
            # but we want to skip unknown.
            for location in range(len(quack_location_type.QuackLocationType)):
                # checks if the location type is type unknown and skips if so.
                if quack_location_type.QuackLocationType(location).name == "unknown":
                    continue
                result = rec.get_playlist(QuackLocationType(location))
        case "range":
            config = load_config("config.cnf")

            track_data = TrackData()
            path = os.path.join(base_folder, "individualSongMetadata", "CompleteIndividualTrackData.csv")
            track_data.load_csv(path)

            range_model = RangeModel(config, track_data)

            range_model.load_track_csv(config.get('RECOMMENDER', 'dataset_csv'))

            rec = RangeRecommender(range_model)

            # For loop that generates the csv files. we could use QuackLocationType instead of numbers,
            # but we want to skip unknown.
            for location in range(len(quack_location_type.QuackLocationType)):
                # checks if the location type is type unknown and skips if so.
                if quack_location_type.QuackLocationType(location).name == "unknown":
                    continue
                rec.get_playlist(QuackLocationType(location), token)
        
        case "machine":
            TaskMaster = Tasks(token)
            TaskMaster.task3_ML_on_kaggle()



if __name__ == "__main__":
    main(sys.argv[1:])
