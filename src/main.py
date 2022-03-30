
from email import header
from operator import index
from playlists_gen import Data_gen
from enum import Enum
import sys
import numpy as np
import pandas as pd
class QuackLocationType(Enum):
    unknown = 0
    church = 1
    education = 2
    cemetery = 3
    forest = 4
    beach = 5
    urban = 6
    night_life = 7

def main(argv):
    #argv=["BQDJ8m31rgfrL9K4XzE5jLo8_JYnkPJvSXYfTeijK2lEoE7t2BIE_NXqlmeBOwGSvZLzjMVkn6nTZWX2cLZ_OqqzxMguu7bRqjj87Zpo7btCTi8XFa6fnlvQFD5XphGgoFUn8b2IgWo6nj2J_jc8WOeb23k_mDkQ5uS3YAM"]
    token: str = argv[0]
    data_gen = Data_gen(token)
    #For loop that generates the csv files. we could use QuackLocationType istead of numbers, but we want to skip unknown.
    # for location in range(1,8):
    #     #gets the search words
    #     words = data_gen.get_searchWords(location)
    #     #gets the track frequency fo the words given
    #     locationtrackFrequency =data_gen.get_trackFrequency(words)
    #     #saves the returned list of 100 songs ids as a csv file in the folder trackFrequencies
    #     locationtrackFrequency.to_csv("trackFrequencies\\"+QuackLocationType(location).name+"Tracks.csv", sep=",", header=False)
    
    allVectorFeatureDataframe = pd.DataFrame()
    #loops through the quack location types again and loads the previously generated csv files in order to generate location feature vectors
    for location2 in range(1, 8):
        #gets the name of the csv file based on the location
        csvfilename = QuackLocationType(location2).name + "Tracks.csv"

        #loads the data from a csv file 
        trackIds = data_gen.load_csvfile(csvfilename)
        #calls get_track_metaData which get the meta data on the top 100 tracks and returns it.
        all_tracks_features = data_gen.get_track_metadata(trackIds)
        #print(all_tracks_features, "\n")

        #calls gen_location_feature_vector which returns a dict of a location feature vector. It is easier to turn a list into a csv file, so the output is converted to a list.
        locationFeatureVector = data_gen.gen_location_feature_vector(all_tracks_features, csvfilename)

        dflocationFeatureVector = pd.DataFrame.from_dict(locationFeatureVector, orient='index', columns=[QuackLocationType(location2).name]).transpose()

        allVectorFeatureDataframe = pd.concat([allVectorFeatureDataframe, dflocationFeatureVector])

        #data_gen.get_individual_song_features(csvfilename, trackIds, all_tracks_features)

    #writes the all the location feature vectors into a single csv file.
    allVectorFeatureDataframe.to_csv("featureVectors\\allLocationFeatureVector.csv", index=True,index_label='locations')



        
if __name__ == "__main__":
    main(sys.argv[1:])
