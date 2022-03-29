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

    def find_playlists(self, location: str, offset = 0):
        # Search for the term "location" and return the first playlist
        result = self._sp.search(location, type="playlist", limit=50, offset= offset)
        # Find the ID of the playlist (nested dict)
        return result

    def get_songs(self, playlist_id: str):
        # Retrieve tracks from the given playlist, only return the track id
        return self._sp.playlist_items(playlist_id)
        
    def get_song_features(self, song_ids: str):
        #retrive meta data on tracks given a specific track id. Returns a list of meta data values
        return self._sp.audio_features(song_ids)