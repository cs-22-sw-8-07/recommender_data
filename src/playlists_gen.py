from cgi import print_directory
from distutils.command.config import config
from itertools import count
from msilib.schema import SelfReg
from typing_extensions import Self
from unittest import result
from webbrowser import get
from numpy import take, var
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import configparser
import os
import sys, getopt
from configparser import ConfigParser
from typing import Optional
from spotify import Spotify
import numpy as np

import collections

def _load_config() -> Optional[ConfigParser]:
        base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        config_file = os.path.join(base_folder, "config.cnf")

        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            print(f"Config file missing... Path should be {config_file}")
            return None

        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        return config

class Data_gen:
    auth_token: str
    spotifyacc: object

    def __init__(self, token):
        self.auth_token = token
        config = _load_config()
        self.spotifyacc = Spotify(config)
        self.spotifyacc.connect_spotify(self.auth_token)
        #self._sp = spotipy.Spotify(auth=token)

        

    def get_searchWords(self, x):
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
                return ["undeath", "undead"]
            case 4:
                #forest
                return ["forest", "woods"]
            case 5:
                #beach
                return ["beach"]
            case 6:
                #urban
                return ["ghetto", "street", "urban"]
            case 7:
                #nigtLife
                return ["bar", "club"]

    def get_trackFrequency(self, searchWords):
        foundPlaylistsId = []
        tracksFrequency = {}
        for word in searchWords:
            for i in range(2):
                # print("\n")
                # print(tracksFrequency)
                #Gets playlists from spotify based on the searchwords, i is the offset.
                findPlaylistResponse = self.spotifyacc.find_playlists(word, i)
                if findPlaylistResponse == None:
                    continue
                findPlaylistResponsePlaylists = findPlaylistResponse["playlists"]
                if findPlaylistResponsePlaylists == None:
                    continue
                playlists = findPlaylistResponsePlaylists["items"]
                if playlists == None:
                    continue
                
                    
                    break
                for j in range(len(playlists)):
                    
                    playlistId = playlists[j]["id"]
                    if playlistId == None:
                        continue
                    if playlistId in foundPlaylistsId:
                        continue
                    if playlistId not in foundPlaylistsId:
                        foundPlaylistsId.append(playlistId)
                        result = self.spotifyacc.get_songs(playlistId)
                        resultItems = result["items"]
                        if resultItems == None:
                            continue
                        
                        for item in resultItems:
                            if item == None:
                                continue
                            itemTrack = item["track"]
                            if itemTrack == None:
                                continue
                            itemTrackId = itemTrack["id"]
                            if itemTrackId == None:
                                continue
                            trackIdllist = [itemTrackId]
                            #print(trackIdllist)

                            for trackId in trackIdllist:
                                if trackId == None:
                                    break
                                if trackId in tracksFrequency:
                                    tracksFrequency[trackId] += 1
                                if trackId not in tracksFrequency:
                                    tracksFrequency[trackId] = 1
                    #if we have less the 50 playlists in the last search we 
                if len(playlists) != 50:
                    print(word, "had", (i*50+len(playlists)), "playlists \n")
                    break
                if i == 1 and len(playlists) == 50:
                    print(word, "had the full", (i*50 + 50), "playlists \n")

        top100Frequencykeyvalue = collections.Counter(tracksFrequency).most_common(100)
        #removes the value in the keyvalue pair and returns a list of track ids
        #top100tracks = [i[0] for i in top100Frequencykeyvalue]
        return top100Frequencykeyvalue

    def get_track_Metadata(self, csvFileName):
        idlist = []
        #Loads the 100 track ids from csv file given as parameter. 
        trackIds = np.loadtxt(csvFileName,delimiter=", ", dtype=str)
        for j in range(len(trackIds)):
            idlist.append(trackIds[j][0])
        all_features = self.spotifyacc.get_song_features(idlist)
        print(all_features[0])
        


                            

                


