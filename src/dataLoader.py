"""
Description: Script that loads the query symbols, training and testing data sets, and labels. 
Inputs:      "dataPath" which is a top level directory which contains the query, training and testing images. "Randomize" which 
             is an optional boolean value determining if the data sets should be randomized or not. 
Returns:     Three lists containing the query, training, and testing images respectively. Two dictionaries comtaining the 
             formatted label information for the training and testing sets.
"""

import sys, cv2, os, random, csv
import numpy as np

# Format the label information in a dictionary for easier handling by the evaluator
def create_label_dict(file_name):
    dictionary = {}

    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            key = row[0]
            pairs = [(int(row[i]),int(row[i+1])) for i in range(1,len(row),2)]
            dictionary[key] = pairs

    return dictionary

def load_data(dataPath,randomize=False):

    if not(dataPath[-1] == '/'):
        dataPath += '/'

    queryFiles = os.listdir(dataPath+"queries/")

    trainingData = os.listdir(dataPath+"train/data/")
    trainingIndices = [x for x in range(0,len(trainingData))]

    testingData = os.listdir(dataPath+"test/data/")
    testingIndices = [x for x in range(0,len(testingData))]

    if randomize:
        random.shuffle(trainingIndices)
        random.shuffle(testingIndices)

    queryImages = []
    testImages = []
    trainImages = []
    testDict = None
    trainDict = None

    # Load query symbols
    for idx in queryFiles:
        imageFileName = dataPath + "queries/" + idx
        queryImages.append(cv2.imread(imageFileName))

    # Load training images and format the labels in a dictionary
    for idx in trainingIndices:
        imageFileName = dataPath + "train/data/" + trainingData[idx]
        trainImages.append(cv2.imread(imageFileName))

        labelFileName = dataPath + "train/label/" + os.path.splitext(trainingData[idx])[0] + ".csv"
        trainDict = create_label_dict(labelFileName)

    # Load testing images and format the labels in a dictionary
    for idx in testingIndices:
        imageFileName = dataPath + "test/data/" + testingData[idx]
        testImages.append(cv2.imread(imageFileName))

        labelFileName = dataPath + "train/label/" + os.path.splitext(testingData[idx])[0] + ".csv"
        testDict = create_label_dict(labelFileName)

    return queryImages, testImages, trainImages, testDict, trainDict
