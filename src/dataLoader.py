"""
Description: Script that loads the query symbols, training and testing data sets, and labels. Prepared the data, calls our 
             symbol spotting algorithm, then passes the results to the evaluate function.

Usage: "python3 dataLoader.py <path/to/data> [randomize]: where <path/to/data> is the top-level directory containing the data, 
             and [randomize] is an optional parameter which specifies that the data set should be handled in a random order.
"""

import sys, cv2, numpy, os, random, csv

def print_usage():
    print("Usage:\n\tpython3 dataLoader.py path/to/data [optional: randomize]")
    exit(0)

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

def main(argv):
    if len(sys.argv) < 2:
        print_usage()

    dataPath = sys.argv[1]

    if not(dataPath[-1] == '/'):
        dataPath += '/'

    if len(sys.argv) > 2:
        randomize = True
    else:
        randomize = False

    queryImages = os.listdir(dataPath+"queries/")

    trainingData = os.listdir(dataPath+"train/data/")
    trainingIndices = [x for x in range(0,len(trainingData))]

    testingData = os.listdir(dataPath+"test/data/")
    testingIndices = [x for x in range(0,len(testingData))]

    if randomize:
        random.shuffle(trainingIndices)
        random.shuffle(testingIndices)

    print("Training set:")
    for idx in trainingIndices:
        imageFileName = trainingData[idx]
        labelFileName = dataPath + "train/label/" + os.path.splitext(imageFileName)[0] + ".csv"
        labelDict = create_label_dict(labelFileName)

        print("File being processed: " + str(imageFileName))
        print("Label: " + str(labelDict))

        # resultDict = awesome_alg(queryImages,imageFileName)
        # metrics = evaluate(labelDict,resultDict)

    print("\nTesting set:")
    for idx in testingIndices:
        imageFileName = testingData[idx]
        labelFileName = dataPath + "train/label/" + os.path.splitext(imageFileName)[0] + ".csv"
        labelDict = create_label_dict(labelFileName)

        print("File being processed: " + str(imageFileName))
        print("Label: " + str(labelDict))

        # resultDict = awesome_alg(queryImages,imageFileName)
        # metrics = evaluate(labelDict,resultDict)


if __name__ == "__main__":
    main(sys.argv)