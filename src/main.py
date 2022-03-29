from playlists_gen import Data_gen
from enum import Enum
import os
import sys, getopt
import numpy as np
import csv
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
    #     #saves the returned list of 100 songs ids as a csv file
    #     np.savetxt(QuackLocationType(location).name+"Tracks.csv", locationtrackFrequency, delimiter=", ", fmt ='% s')

    csvdictfields = ["danceability", "energy", "key", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "tempo"]

    for location2 in range(1,8):
        csvfilename = QuackLocationType(location2).name + "Tracks.csv"
        locationFeatureVector = list(data_gen.get_track_Metadata(csvfilename).items())
        print(locationFeatureVector)
        np.savetxt("featureVectors\\" + QuackLocationType(location2).name+"LocationFeatureVector.csv", locationFeatureVector, delimiter=", ", fmt ='% s')

        
if __name__ == "__main__":
    main(sys.argv[1:])
