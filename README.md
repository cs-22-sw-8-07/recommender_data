Add a file "recommender_data/config.cnf" with contents:
```
[RECOMMENDER]
test_mode=false
client_id=
client_secret=
dataset_csv=
[RANGE_MODEL]
slice_percentage=0.4
no_of_range_attributes=4
```
Get "client_id" and "client_secret" from the developers.

The "dataset_csv" should contain the path to a kaggle dataset. To get the kaggle dataset, download it from our shared drive folder under "Resourcer", or download it directly from kaggle: https://www.kaggle.com/datasets/lehaknarnauli/spotify-datasets?select=tracks.csv

In order to run you need 2 arguments.
1. argument is a spotify acces key.
2. argument is the model that should be run. SO far you can choose between "dataset", "range" and "distance".

The output of each model can be found in:
- "dataset": trackFrequency and featureVector
- "range": range_recommender_tracks
- "distance": distance_recommender_tracks
