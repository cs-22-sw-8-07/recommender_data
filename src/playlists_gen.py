from distutils.command.config import config
import json
from msilib.schema import SelfReg
from typing_extensions import Self
from numpy import var
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import configparser
import os
import sys, getopt
from configparser import ConfigParser
from typing import Optional

from spotify import Spotify

def _load_config() -> Optional[ConfigParser]:
        base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        config_file = os.path.join(base_folder, "config.cnf")

        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            print(f"Config file missing... Path should be {config_file}")
            return None

        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        return config

class Playlist_gen():
    auth_token: str
    spotifyacc: var

    def __init__(self, token):
        self.auth_token = token
        config = _load_config()
        spotifyacc = Spotify(config)
        spotifyacc.connect_spotify(self.auth_token)
    
    
    def get_searchwords(x):
        match x:
            #search words on spotify for each location type. very rough
            case 1:
                #church
                return ["church", "christ"]
            case 2:
                #education
                return ["university"]
            case 3:
                #cemetery
                return ["graveyard", "cemetery"]
            case 4:
                #forest
                return ["forest", "woods"]
            case 5:
                #beach
                return ["beach"]
            case 6:
                #urban
                return ["urban", "street"]
            case 7:
                #nigtLife
                return ["bar", "club"]

    def get_playlist(searchword):
        for word in searchword:
            for i in range(20):
                print("hello")



            

            

