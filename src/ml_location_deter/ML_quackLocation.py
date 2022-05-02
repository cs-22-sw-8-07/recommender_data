from distutils.ccompiler import show_compilers
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
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from keras.layers import Dense
from keras import regularizers
from sklearn.ensemble import VotingClassifier
from keras.utils.vis_utils import plot_model

class AddLocationtoKaggle:


    def loadCSVfileML(path):
        return pd.read_csv(path, usecols=["id","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","time_signature","location"])
        

    def trainModelSingle(x_train, y_train, x_test, y_test):
        
        model = Sequential()
        model.add(Dense(20, input_dim=x_train.shape[1], activation='relu' ))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(len((QuackLocationType))-1, activation='softmax'))

        adam  = tf.keras.optimizers.Adam(learning_rate=1e-3)
        model.compile(optimizer=adam, loss=keras.losses.CategoricalCrossentropy(), metrics = ['accuracy'])

        history = model.fit(x_train, y_train, epochs=50, validation_data = (x_test, y_test))
        
        cross_val_score
        
        return model

    def trainModelKFold(traindata, target):

        num_folds = 10
        # Define the K-fold Cross Validator
        kfold = KFold(n_splits=num_folds, shuffle=True)

        # K-fold Cross Validation model evaluation
        # Define the K-fold Cross Validator
        kfold = KFold(n_splits=num_folds, shuffle=True)
        accuracy_per_fold = []
        # K-fold Cross Validation model evaluation
        fold_no = 1
        for train_index, test_index in kfold.split(traindata, target):
        
            x_train = traindata.iloc[train_index]
            y_train = target.iloc[train_index]
            x_test = traindata.iloc[test_index]
            y_test = target.iloc[test_index]

            model = Sequential()
            model.add(Dense(10, input_dim=x_train.shape[1], activation='relu', kernel_regularizer=keras.regularizers.l2(1e-4)))
            model.add(Dense(10, activation='relu', kernel_regularizer=keras.regularizers.l2(1e-4)))
            model.add(Dense(len((QuackLocationType))-1, activation='softmax'))
            
            adam  = tf.keras.optimizers.Adam(learning_rate=1e-3)
            model.compile(optimizer=adam, loss=keras.losses.CategoricalCrossentropy(), metrics = ['accuracy'])

            print("training on fold number", fold_no)
            history = model.fit(x_train, y_train, epochs=500, validation_data = (x_test, y_test))
            scores = model.evaluate(x_test, y_test, verbose=0)
            accuracy_per_fold.append(scores[1] * 100)

            #saving models in their own folder named based on which fold. 
            model_save_location ='../recommender_data/ml_models/model_foldnum_' + str(fold_no)
            model.save(model_save_location)

            fold_no = fold_no +1
        
        print(accuracy_per_fold)
        print("accuracy for the whole model = ", sum(accuracy_per_fold)/len(accuracy_per_fold))
        

        #loading the top 1 best models
        top_acc_index = sorted(range(len(accuracy_per_fold)), key=lambda x: accuracy_per_fold[x])[-1:]

        model1 = keras.models.load_model('../recommender_data/ml_models/model_foldnum_' + str(top_acc_index[0]+1))

        return model1
    
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

    def skim_kaggle_dataset(kaggle_dataset):
        kaggle_dataset = kaggle_dataset[kaggle_dataset.speechiness < 0.66]
        kaggle_dataset = kaggle_dataset[kaggle_dataset.liveness < 0.8]
        kaggle_dataset = kaggle_dataset[kaggle_dataset.energy < 0.9]
        kaggle_dataset = kaggle_dataset[kaggle_dataset.energy > 0.1]
        kaggle_dataset = kaggle_dataset[kaggle_dataset.acousticness < 0.9]
        return kaggle_dataset

        #kaggle_dataset = kaggle_dataset.drop(kaggle_dataset[].index)

