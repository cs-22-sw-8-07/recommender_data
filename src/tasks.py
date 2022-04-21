
from lib2to3.pgen2 import token
import quackLocationType
from playlists_gen import Data_gen
import pandas as pd
from asyncio import tasks
from operator import index
import numpy as np
import quackLocationType
import os

class Tasks:
    data_gen: object

    def __init__(self, token: str):
        self.data_gen = Data_gen(token)
        
    def task1_trackFrequencies(self):
        #this is the number of songs saved to the csv file. 
        numberTopSongs = 200
        #For loop that generates the csv files. we could use QuackLocationType istead of numbers, but we want to skip unknown.
        for location in range(len(quackLocationType.QuackLocationType)):
            #checks if the location type is type unknown and skips if so. 
            if(quackLocationType.QuackLocationType(location).name == "unknown"):
                continue
            #gets the search words
            words = self.data_gen.get_searchWords(location)
            #gets the track frequency fo the words given
            locationtrackFrequency =self.data_gen.get_trackFrequency(words, numberTopSongs)
            #saves the returned list of 100 songs ids as a csv file in the folder trackFrequencies
            locationtrackFrequency.to_csv(os.path.join("trackFrequencies", quackLocationType.QuackLocationType(location).name + "Tracks.csv"), sep=",", header=False)
    
    def task2_featureVectorsAndIndividualTracks(self):
        allVectorFeatureDataframe = pd.DataFrame()
        completeIndividualTrackData = pd.DataFrame()
        #loops through the quack location types again and loads the previously generated csv files in order to generate location feature vectors
        for location in range(len(quackLocationType.QuackLocationType)):
            #checks if the location type is type unknown and skips if so. 
            if(quackLocationType.QuackLocationType(location).name == "unknown"):
                continue
            #gets the name of the csv file based on the location
            csvfilename = quackLocationType.QuackLocationType(location).name + "Tracks.csv"

            #loads the data from a csv file 
            trackIds = self.data_gen.load_csvfile(csvfilename)
            #calls get_track_metaData which get the meta data on the top 100 tracks and returns it.
            all_tracks_features = self.data_gen.get_track_metadata(trackIds)
            
            #calls gen_location_feature_vector which returns a dict of a location feature vector. It is easier to turn a list into a csv file, so the output is converted to a list.
            locationFeatureVector = self.data_gen.gen_location_feature_vector(all_tracks_features, csvfilename)
            #turns locationFeatureVector into a dataframe in order to more easily turn it into a csv. 
            dflocationFeatureVector = pd.DataFrame.from_dict(locationFeatureVector, orient='index', columns=[quackLocationType.QuackLocationType(location).name]).transpose()

            #appends all the feature vectors together into a single file/variable
            allVectorFeatureDataframe = pd.concat([allVectorFeatureDataframe, dflocationFeatureVector])

            #calls get_individual_song_features and gets all the invidiual tracks metadata into a single file. It is formated in order to match the kaggle dataset. 
            locationTracksMetadata = self.data_gen.get_individual_song_features(csvfilename, trackIds, all_tracks_features, quackLocationType.QuackLocationType(location).name)
            #appends the individual song metadata for each location into a single file. 
            completeIndividualTrackData = pd.concat([completeIndividualTrackData,locationTracksMetadata])

        #writes the all the location feature vectors into a single csv file.
        allVectorFeatureDataframe.to_csv(os.path.join("featureVectors", "allLocationFeatureVector.csv"), index=True,index_label='locations')
        #write all the individual track metadata into a csv file.
        completeIndividualTrackData.to_csv(os.path.join("individualSongMetadata","CompleteIndividualTrackData.csv"),index=True,index_label='id')