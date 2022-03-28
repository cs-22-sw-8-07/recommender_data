from playlists_gen import Playlist_gen
from enum import Enum
import os
import sys, getopt
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
    playlist_gen = Playlist_gen(token)
    #we could use QuackLocationType but we want to skip unknown.
    for location in range(1, 8):
        #gets the search words
        
        words = playlist_gen.get_searchwords(location)
        #gets the track frequency fo the words given
        locationtrackFrequency =playlist_gen.get_trackFrequency(words)
        np.savetxt(QuackLocationType(location).name+"Tracks.csv", locationtrackFrequency, delimiter=", ", fmt ='% s')

if __name__ == "__main__":
    main(sys.argv[1:])
