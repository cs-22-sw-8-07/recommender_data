# recommender_data

In order to run you need 1 arguments. first argument is you spotify access key. 
The default is set to 50 playlist per searchwords. The number for each searchword is print.
The number of songs used to find the location feature vector is also printed as some songs do not have metadata. 

The output of this script are found in trackFrequencies and featureVectors folders. These are csv files with a list of the most frequent songs in the playlists for each location and the average metadata values for each location, repectivly. 