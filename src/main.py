from playlists_gen import Data_gen
from enum import Enum
import sys
import numpy as np
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
    #     np.savetxt("trackFrequencies\\"+QuackLocationType(location).name+"Tracks.csv", locationtrackFrequency, delimiter=", ", fmt ='% s')
    
    #loops through the quack location types again and loads the previously generated csv files in order to generate location feature vectors
    for location2 in range(1, 8):
        print(location2)
        #loads the csv file
        csvfilename = QuackLocationType(location2).name + "Tracks.csv"
        #calls get_track_metaData which returns a dict. It is easier to turn a list into a csv file, so the output is converted to a list.
        locationFeatureVector = list(data_gen.get_track_metadata(csvfilename).items())
        #saves the list to a csv file in the featureVectors folder
        np.savetxt("featureVectors\\" + QuackLocationType(location2).name+"LocationFeatureVector.csv", locationFeatureVector, delimiter=", ", fmt ='% s')

        
if __name__ == "__main__":
    main(sys.argv[1:])
