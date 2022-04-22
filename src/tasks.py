from cgi import test
from lib2to3.pgen2 import token
from quack_location_type import QuackLocationType
from playlists_gen import Data_gen
from asyncio import tasks
from operator import index
import quack_location_type
import os
from ml_location_deter.ML_quackLocation import AddLocationtoKaggle
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Tasks:
    data_gen: object

    def __init__(self, token: str):
        self.data_gen = Data_gen(token)

    def task1_trackFrequencies(self):
        #this is the number of songs saved to the csv file.
        numberTopSongs = 200
        #For loop that generates the csv files. we could use QuackLocationType istead of numbers, but we want to skip unknown.
        for location in range(len(QuackLocationType)):
            #checks if the location type is type unknown and skips if so.
            if(QuackLocationType(location).name == "unknown"):
                continue
            # gets the search words
            words = self.data_gen.get_searchWords(location)
            # gets the track frequency fo the words given
            locationtrackFrequency = self.data_gen.get_trackFrequency(words, numberTopSongs)
            # saves the returned list of 100 songs ids as a csv file in the folder trackFrequencies
            locationtrackFrequency.to_csv(
                os.path.join("trackFrequencies", quack_location_type.QuackLocationType(location).name + "Tracks.csv"),
                sep=",", header=False)

    def task2_featureVectorsAndIndividualTracks(self):
        allVectorFeatureDataframe = pd.DataFrame()
        completeIndividualTrackData = pd.DataFrame()
        # loops through the quack location types again and loads the previously generated csv files in order to generate location feature vectors
        for location in range(len(quack_location_type.QuackLocationType)):
            # checks if the location type is type unknown and skips if so.
            if (quack_location_type.QuackLocationType(location).name == "unknown"):
                continue
            # gets the name of the csv file based on the location
            csvfilename = quack_location_type.QuackLocationType(location).name + "Tracks.csv"

            # loads the data from a csv file
            trackIds = self.data_gen.load_csvfile(csvfilename)
            # calls get_track_metaData which get the meta data on the top 100 tracks and returns it.
            all_tracks_features = self.data_gen.get_track_metadata(trackIds)

            #calls gen_location_feature_vector which returns a dict of a location feature vector. It is easier to turn a list into a csv file, so the output is converted to a list.
            locationFeatureVector = self.data_gen.gen_location_feature_vector(all_tracks_features, csvfilename)
            # turns locationFeatureVector into a dataframe in order to more easily turn it into a csv.
            dflocationFeatureVector = pd.DataFrame.from_dict(locationFeatureVector, orient='index', columns=[
                quack_location_type.QuackLocationType(location).name]).transpose()

            # appends all the feature vectors together into a single file/variable
            allVectorFeatureDataframe = pd.concat([allVectorFeatureDataframe, dflocationFeatureVector])

            # calls get_individual_song_features and gets all the invidiual tracks metadata into a single file. It is formated in order to match the kaggle dataset.
            locationTracksMetadata = self.data_gen.get_individual_song_features(csvfilename, trackIds,
                                                                                all_tracks_features,
                                                                                quack_location_type.QuackLocationType(
                                                                                    location).name)
            # appends the individual song metadata for each location into a single file.
            completeIndividualTrackData = pd.concat([completeIndividualTrackData, locationTracksMetadata])

        # writes the all the location feature vectors into a single csv file.
        allVectorFeatureDataframe.to_csv(os.path.join("featureVectors", "allLocationFeatureVector.csv"), index=True,
                                         index_label='locations')
        # write all the individual track metadata into a csv file.
        completeIndividualTrackData.to_csv(os.path.join("individualSongMetadata", "CompleteIndividualTrackData.csv"),
                                           index=True, index_label='id')
    
    def task3_ML_on_kaggle(self):
        ml = AddLocationtoKaggle
        pathTrain = "../recommender_data/individualSongMetadata/CompleteIndividualTrackData200.csv"
        pathPred = "../recommender_data/individualSongMetadata/tracks.csv"
        fullcsv = ml.loadCSVfileML(pathTrain)
        target = pd.get_dummies(fullcsv['location'])
        
        trainData = ml.ML_preprocessing(fullcsv)

        x_train, x_test, y_train, y_test = train_test_split(trainData, target, test_size=0.1)


        model = ml.trainModel(x_train, y_train, x_test, y_test)
        #ml.showConfusionMatrix(model,x_test,y_test)

        kaggle_dataset = pd.read_csv(pathPred, usecols=["id", "name","artists","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","time_signature"])

        print(kaggle_dataset, "\n \n")

        kaggle_predset = ml.ML_preprocessing(kaggle_dataset)

        print(kaggle_predset, "\n \n")

        testing = model.predict(kaggle_predset)

        print(testing, "\n \n")
        print(len(testing))

        
