from multiprocessing.connection import wait
from time import time
from unicodedata import name
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
from time import sleep
from sklearn.model_selection import KFold, StratifiedKFold

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
        num_folds = 10
        
        pathTrain = "../recommender_data/individualSongMetadata/CompleteIndividualTrackData200.csv"
        pathPred = "../recommender_data/individualSongMetadata/skimmed_tracks.csv"
        fullcsv = ml.loadCSVfileML(pathTrain)
        target = pd.get_dummies(fullcsv['location'])
        
        #creates the training data and preproccesses  loudness and tempo with normalization. 
        trainData = ml.ML_preprocessing(fullcsv)

        

        #x_train, x_test, y_train, y_test = train_test_split(trainData, target, test_size=0.1)


        #model = ml.trainModelSingle(x_train, y_train, x_test, y_test)
        model = ml.trainModelKFold(trainData, target)
        #ml.showConfusionMatrix(model,x_test,y_test)

        kaggle_dataset = pd.read_csv(pathPred, usecols=["id", "name","artists","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","time_signature"])

        #removes garbage from kaggledataset and creates file skimmed_tracks.csv
        kaggle_dataset = ml.skim_kaggle_dataset(kaggle_dataset)
        kaggle_dataset.to_csv(
                os.path.join("individualSongMetadata", "skimmed_tracks.csv"),
                sep=",", header=True, index=False)


        #preprocesses the kaggle dataset
        kaggle_predset = ml.ML_preprocessing(kaggle_dataset)
        #predicts on the kaggle dataset
        predicted_values = model.predict(kaggle_predset)
        predicted_values =predicted_values.tolist()
        location_value = [0] * len(predicted_values)
        location_enum = [0] * len(predicted_values)
        #takes the id name and artists from the kaggledataset. the predicted kaagleset is the data that is later turned into csv files. 
        predicted_kaggleset = kaggle_dataset[["id", "name","artists"]]
        
        #goes through every predicted set of values and finds the highest percentage location value. This percentage is then saved for ordering later and we use the quacklocationtype enum to get the actual location. The +1 is used to skip the unknown category. 
        for listnum in range(len(predicted_values)):
            location_value[listnum] = max(predicted_values[listnum])
            location_enum[listnum] = quack_location_type.QuackLocationType(predicted_values[listnum].index(max(predicted_values[listnum]))+1).name

            

        #adds location and the percantage location value to our dataset. 
        predicted_kaggleset.loc[:,"location"] = location_enum
        predicted_kaggleset.loc[:,"location_value"] = location_value
        #sorts the dataframe based on the location value.
        predicted_kaggleset = predicted_kaggleset.sort_values('location_value', ascending=False)
        
        for locationint in range(len(quack_location_type.QuackLocationType)):
            image_list = [] * 1000
            #if unknown continue. 
            if locationint == 0:
                continue
            #splits the dataset into 7 based their respective locations and only takes highest 1000 location values
            predicted_location_tracks =predicted_kaggleset.loc[predicted_kaggleset['location'] == quack_location_type.QuackLocationType(locationint).name].head(1000)
            #drops location and location value as these are not needed anymore and are not part of the final csv.
            predicted_location_tracks = predicted_location_tracks.drop(columns=['location', 'location_value'])
            artist_string_list = []
            for id in predicted_location_tracks['id']:
                #gets the image for every id in the dataframe
                image_list.append(self.data_gen.get_track_image(id))

                #turns the artist field into the correct form.
                artists_series = predicted_location_tracks.loc[predicted_location_tracks['id'] == id, 'artists']
                artist_list = artists_series.iloc[0].split(",")
                artists = ";".join(artist_list)
                artists = artists.replace("[","")
                artists = artists.replace("]","")
                artists = artists.replace("'","")
                artist_string_list.append(artists)
                #predicted_kaggleset.loc[predicted_kaggleset['id'] == id, 'artists'] = artists
            predicted_location_tracks['artists']= artist_string_list

            #appends the images to the dataframe. 
            predicted_location_tracks.loc[:,'image'] = image_list
            predicted_location_tracks.to_csv(
                os.path.join("machinelearn_recommender_tracks", quack_location_type.QuackLocationType(locationint).name + "_tracks.csv"),
                sep=",", header=False, index=False)
            print(quack_location_type.QuackLocationType(locationint).name + " pictures fetched \n")
            sleep(10)
            #print(predicted_kaggleset.loc[predicted_kaggleset['location'] == 'night_life'])
        
