import json
import uuid
from enum import Enum


class Errors(Enum):
    NoConfigFile = 105
    CouldNotInitializeRecommender = 109
    CouldNotInitializeSpotipy = 110
    CouldNotInitializeVectorSpace = 111
    CouldNotFindClosestTracks = 112
    CouldNotFindSongsFromPlaylist = 113
    CouldNotFormatSongListToJson = 114
    QuackLocationTypeArgumentNotANumber = 115
    QuackLocationTypeNotWithinRange = 116
    CouldNotFindTracksFromRangeRecommender = 117
    CouldNotInitializeRangeModel = 118
    CouldNotLoadDataSet = 119
    CouldNotInitializeVectorSpaceModel = 120
    Argument3NotGiven = 121
    Argument3NotARecommender = 122
    CouldNotLoadTrackData = 123
    CouldNotCreateCSVFile = 124


def service_response_error_json(error_no: int):
    parsed_result = {
        "is_successful": 0,
        "error_no": error_no,
        "error_msg": Errors(error_no).name
    }
    return json.dumps(parsed_result, indent=4)


def service_response_playlist_json(tracks, location):
    parsed_result = {
        "result": {
            "id": str(uuid.uuid4()),
            "location_type": location,
            "tracks": tracks
        },
        "is_successful": 1,
        "error_no": 0
    }
    return json.dumps(parsed_result)
