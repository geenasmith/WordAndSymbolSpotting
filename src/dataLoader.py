"""
Description: Script that loads the query symbols, data set, and labels. 
Inputs:      "dataPath" which is a top level directory which contains the query, data images, and labels. "Randomize" which 
             is an optional boolean value determining if the data set should be randomized or not. 
Returns:     Two lists containing the query, and data images respectively. One dictionary comtaining the 
             formatted label information for the data set.
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

    data = os.listdir(dataPath+"data/")
    dataIndices = [x for x in range(0,len(data))]

    if randomize:
        random.shuffle(dataIndices)

    queryImages = []
    dataImages = []
    dataDict = None

    # Load query symbols
    for idx in queryFiles:
        imageFileName = dataPath + "queries/" + idx
        queryImages.append(cv2.imread(imageFileName))


    # Load images and format the labels in a dictionary
    for idx in dataIndices:
        imageFileName = dataPath + "data/" + data[idx]
        dataImages.append(cv2.imread(imageFileName))

        labelFileName = dataPath + "label/" + os.path.splitext(data[idx])[0] + ".csv"
        dataDict = create_label_dict(labelFileName)

    return queryImages, dataImages, dataDict
