from cgi import print_directory
from itertools import count
from msilib.schema import SelfReg
from webbrowser import get
from numpy import take, var
import configparser
import os
from configparser import ConfigParser
from typing import Optional
from spotify import Spotify
import numpy as np
import pandas as pd

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
        tracksFrequency = pd.DataFrame()
        #Choose how many playlists are found and used. The number of playlist are searchIterations*50
        searchIterations = 1
        for word in searchWords:
            for i in range(searchIterations):
                # print("\n")
                # print(tracksFrequency)
                #Gets playlists from spotify based on the searchwords, i is the offset. You can also add another parameter limit which sets the number of playlists found. Default is 50.
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
                    #Checks if the playlist already have been found before. If true we skip the playlist
                    if playlistId in foundPlaylistsId:
                        continue
                    #Sets the playlist as found and gets all the songs in the playlist from spotify and saves it to result
                    if playlistId not in foundPlaylistsId:
                        foundPlaylistsId.append(playlistId)
                        result = self.spotifyacc.get_songs(playlistId)
                        resultItems = result["items"]
                        if resultItems == None:
                            continue
                        
                        for item in resultItems:
                            #checks to make sure we don't end up with errors. 
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
                                #if track was found before increment its value by one. if not then declare a new key value pair with the id. 
                                if itemTrack["track"] == False:
                                    continue
                                if trackId in tracksFrequency.index:
                                    tracksFrequency.at[trackId,'frequency'] += 1
                                if trackId not in tracksFrequency.index:
                                    tempdf = pd.DataFrame({'frequency': 1,'popularity': itemTrack['popularity']}, index=[trackId],columns=['frequency', 'popularity'])
                                    tracksFrequency = pd.concat([tracksFrequency,tempdf], axis= 0)
                #if we have less the 50 playlists in the last search we 
                if len(playlists) != 50:
                    print(word, "had", (i*50+len(playlists)), "playlists \n")
                    break
                if i == (searchIterations-1) and len(playlists) == 50:
                    print(word, "had the full", (i*50 + 50), "playlists \n")

        top100dataframe = tracksFrequency.nlargest(100, 'frequency')
        #turns the list into a dataframe
        #top100dataframe = pd.DataFrame(top100Frequencykeyvalue, columns=['id', 'frequency', 'popularity'])
        
        return top100dataframe

    def load_csvfile(self, csvFileName):
        #Loads the 100 track ids from csv file given as parameter from the folder trackFrequencies. 
        return pd.read_csv("trackFrequencies\\"+csvFileName, header=None)

    def get_track_metadata(self,trackIds):
        #gets the id of all the songs
        idlist = list(trackIds.loc[:,0])
            #returns the song features
        return self.spotifyacc.get_song_features(idlist)

    def gen_location_feature_vector(self, all_tracks_Features, csvFileName):
        totalAggregatedFeatures = {}

        #the number we divide by in the end
        songsWithData = len(all_tracks_Features)
        #initializes all the dict key values pairs. 
        totalAggregatedFeatures["danceability"] = 0
        totalAggregatedFeatures["energy"] = 0
        #totalAggregatedFeatures["key"] = 0
        totalAggregatedFeatures["loudness"] = 0
        totalAggregatedFeatures["speechiness"] = 0
        totalAggregatedFeatures["acousticness"] = 0
        totalAggregatedFeatures["instrumentalness"] = 0
        totalAggregatedFeatures["liveness"] = 0
        totalAggregatedFeatures["tempo"] = 0
        totalAggregatedFeatures["valence"] =0
        
        #Goes through all the features and aggregates them into seperate variables
        for num in range(len(all_tracks_Features)):
            current_Features = all_tracks_Features[num]

            #Checks if the song actually have any metadata. If not we skip it and reduce the number we divide by 1
            if(current_Features == None):
                songsWithData -= 1
                continue

            totalAggregatedFeatures["danceability"] += current_Features["danceability"]
            totalAggregatedFeatures["energy"] += current_Features["energy"]
            #totalAggregatedFeatures["key"] += current_Features["key"] #should probably not use. Music theory stuff. Ask Jonas if you want to know. 
            totalAggregatedFeatures["loudness"] += current_Features["loudness"]
            totalAggregatedFeatures["speechiness"] += current_Features["speechiness"]
            totalAggregatedFeatures["acousticness"] += current_Features["acousticness"]
            totalAggregatedFeatures["instrumentalness"] += current_Features["instrumentalness"]
            totalAggregatedFeatures["liveness"] += current_Features["liveness"]
            totalAggregatedFeatures["tempo"] += current_Features["tempo"]
            totalAggregatedFeatures["valence"] += current_Features["valence"]
        
        
        print("there were", songsWithData, "songs with eligeble data in", csvFileName)
        #find the mean value for every feature. basically divides the sum by 100
        for feature in totalAggregatedFeatures:
            totalAggregatedFeatures[feature] = totalAggregatedFeatures[feature]/songsWithData
        return totalAggregatedFeatures
        
    def get_individual_song_features(self, csvfilename, trackIds, all_tracks_features):
        print("lol")
 

            


        


                            

                


