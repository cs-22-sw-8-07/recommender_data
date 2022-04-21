from tasks import Tasks
import sys

def main(argv):

    token: str = argv[0]

    TaskMaster = Tasks(token)
    #generates the track frequencies csv files.
    #TaskMaster.task1_trackFrequencies()

    #generates the completed feature vectors and the invidual song meta data csv files. 
    TaskMaster.task2_featureVectorsAndIndividualTracks()


        
if __name__ == "__main__":
    main(sys.argv[1:])
