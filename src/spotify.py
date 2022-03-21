from http import client
import json
import spotipy
from configparser import ConfigParser
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify:
    _client_id: str

    def __init__(self, config: ConfigParser):
        self._config = config
        self._client_id = self._config.get('RECOMMENDER', 'client_id')
        self._client_secret = self._config.get('RECOMMENDER', 'client_secret')
        self._sp = None
    
    def connect_spotify(self, auth_token: str):
        if self._sp is None:
            # Authorize via spotify and save the auth token in _sp
            self._sp = spotipy.Spotify(auth=auth_token)

    def find_playlist_id(self, location: str, offset = 0):
        # Search for the term "location" and return the first playlist
        result = self._sp.search(location, type="playlist", limit=50, offset= offset)
        # Find the ID of the playlist (nested dict)
        return result["playlists"]["items"][0]["id"]

    def get_songs(self, playlist_id: str):
        # Retrieve tracks from the given playlist, only return the track id
        result = self._sp.playlist_items(playlist_id, limit=10)

        # Find the track ID of every track in the dict, and add them to an array
        tracks = []
        for item in result["items"]:
            # Add all artists to one string, comma seperated
            artist_list = []
            for artist in item["track"]["artists"]:
                artist_list.append(artist["name"])
            artists = ", ".join(artist_list)

            # Find the image URL of the smallest available cover art image
            images = item["track"]["album"]["images"]
            images_sorted = sorted(images, key=lambda d: d["width"])
            image_url = images_sorted[0]["url"]

            # Format the track with the necessary info
            track_dict = {
                "id": item["track"]["id"],
                "name": item["track"]["name"],
                "artist": artists,
                "image": image_url
            }
            tracks.append(track_dict)

        parsed_result = {
            "result": {
                "id": "placeholder",
                "location_type": "placeholder",
                "tracks": tracks
            },
            "is_successful": "placeholder",
            "error_no": 0
        }

        return json.dumps(parsed_result, indent=4)