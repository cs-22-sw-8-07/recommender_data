from ntpath import join
from sklearn import metrics
import tensorflow as tf
import pandas as pd
import numpy as np
from tqdm import tqdm 
from keras.models import Sequential
import keras.layers
from quack_location_type import QuackLocationType
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing

class AddLocationtoKaggle:


    def loadCSVfileML(path):
        return pd.read_csv(path, usecols=["id","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","time_signature","location"])
        

    def trainModel(x_train, y_train, x_test, y_test):

        inputs = keras.Input(shape=x_train.shape[1])
        hidden_layer = keras.layers.Dense(x_train.shape[1], activation="relu")(inputs)
        output_layer = keras.layers.Dense(len(QuackLocationType)-1, activation="softmax")(hidden_layer)

        model = keras.Model(inputs=inputs, outputs=output_layer)
        adam  = tf.keras.optimizers.Adam(learning_rate=1e-3)
        model.compile(optimizer=adam, loss=keras.losses.CategoricalCrossentropy(), metrics = ['accuracy'])

        history = model.fit(x_train, y_train, epochs=50, validation_data = (x_test, y_test))
        
        
        return model
    
    def showConfusionMatrix(model,x_test,y_test):
        y_pred = model.predict(x_test)
        prediction = pd.DataFrame(y_pred, columns=y_test.columns)
        
        true_location = y_test.idxmax(axis="columns")
        predicted_location = prediction.idxmax(axis="columns")

        matrix = confusion_matrix(true_location, predicted_location)
        confusion_df = pd.DataFrame(matrix, index=y_test.columns.values, columns=y_test.columns.values)

        # Set the names of the x and y axis, this helps with the readability of the heatmap.
        confusion_df.index.name = 'True Label'
        confusion_df.columns.name = 'Predicted Label'
        sns.heatmap(confusion_df, annot=True)
        plt.show()

    def ML_preprocessing(fullcsv):

        trainData = fullcsv[["danceability","energy","speechiness","acousticness","instrumentalness","liveness","valence", "mode"]]
        normalizeValues = fullcsv[["loudness","tempo"]]
    
        #normalize all the values in the dataframe. first by transforming it into a array.
        x = normalizeValues.values
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        #turn the normailzed values back into a dataframe
        normalizedValues = pd.DataFrame(x_scaled, columns=["loudness","tempo"])
        trainData = trainData.join(normalizedValues, on = trainData.index)
        
        return trainData