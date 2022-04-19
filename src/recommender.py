from quack_location_type import QuackLocationType
from service_response import service_response_playlist_json


class Recommender:
    def __init__(self):
        pass

    def get_playlist(self, location: QuackLocationType):
        raise Exception("Cannot call base class")

    def _get_playlist_json(self, tracks, location: QuackLocationType):
        # Find the track ID of every track in the dict, and add them to an array
        tracks_formatted = []
        for track in tracks:
            # Add all artists to one string, comma seperated
            artist_list = []
            for artist in track.artists:
                artist_list.append(artist)
            artists = ", ".join(artist_list)

            # Format the track with the necessary info
            track_dict = {
                "id": track.id,
                "name": track.name,
                "artist": artists,
                "image": "none"
            }
            tracks_formatted.append(track_dict)

        return service_response_playlist_json(tracks_formatted, location.name)
