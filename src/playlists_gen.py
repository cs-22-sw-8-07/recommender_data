from cgi import print_directory
from msilib.schema import SelfReg
from webbrowser import get
from numpy import take, var
import configparser
import os
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

        

    def get_searchWords(self, x):
        match x:
            #search words on spotify for each location type. very rough
            case 1:
                #church
                return ["church", "christ", "god", "jesus"]
            case 2:
                #education
                return ["university", "study", "class"]
            case 3:
                #cemetery
                return ["crypt", "tomb NOT tomboy", "grave", "cemetery"]
            case 4:
                #forest
                return ["forest", "woods", "wildlife", "nature"]
            case 5:
                #beach
                return ["beach", "sun", "summer", "heat"]
            case 6:
                #urban
                return ["ghetto", "street", "urban"]
            case 7:
                #nigtLife
                return ["bar", "club", "party", "night"]


    def get_trackFrequency(self, searchWords):
        foundPlaylistsId = []
        tracksFrequency = {}
        searchiterations = 1
        for word in searchWords:
            for i in range(searchiterations):
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
                if i == (searchiterations-1) and len(playlists) == 50:
                    print(word, "had the full", (i*50 + 50), "playlists \n")

        top100Frequencykeyvalue = collections.Counter(tracksFrequency).most_common(100)
        #removes the value in the keyvalue pair and returns a list of track ids
        #top100tracks = [i[0] for i in top100Frequencykeyvalue]
        return top100Frequencykeyvalue


    def get_track_metadata(self, csvFileName):
        idlist = []
        totalAggregatedFeatures = {}

        #Loads the 100 track ids from csv file given as parameter from the folder trackFrequencies. 
        trackIds = np.loadtxt("trackFrequencies\\"+csvFileName,delimiter=", ", dtype=str)
        for j in range(len(trackIds)):
            idlist.append(trackIds[j][0])
        all_Features = self.spotifyacc.get_song_features(idlist)
        

        #initializes all the dict key values pairs. 
        totalAggregatedFeatures["danceability"] = 0
        totalAggregatedFeatures["energy"] = 0
        totalAggregatedFeatures["key"] = 0
        totalAggregatedFeatures["loudness"] = 0
        totalAggregatedFeatures["speechiness"] = 0
        totalAggregatedFeatures["acousticness"] = 0
        totalAggregatedFeatures["instrumentalness"] = 0
        totalAggregatedFeatures["liveness"] = 0
        totalAggregatedFeatures["tempo"] = 0

        #Goes through all the features and aggregates them into seperate variables
        for num in range(len(trackIds)):
            current_Features = all_Features[num]
            totalAggregatedFeatures["danceability"] += current_Features["danceability"]
            totalAggregatedFeatures["energy"] += current_Features["energy"]
            totalAggregatedFeatures["key"] += current_Features["key"] #should probably not use. Music theory stuff. Ask Jonas if you want to know. 
            totalAggregatedFeatures["loudness"] += current_Features["loudness"]
            totalAggregatedFeatures["speechiness"] += current_Features["speechiness"]
            totalAggregatedFeatures["acousticness"] += current_Features["acousticness"]
            totalAggregatedFeatures["instrumentalness"] += current_Features["instrumentalness"]
            totalAggregatedFeatures["liveness"] += current_Features["liveness"]
            totalAggregatedFeatures["tempo"] += current_Features["tempo"]
        
        #find the mean value for every feature. basically divides the sum by 100
        for feature in totalAggregatedFeatures:
            totalAggregatedFeatures[feature] = totalAggregatedFeatures[feature]/len(trackIds)
        return totalAggregatedFeatures
        
 

            


        


                            

                


