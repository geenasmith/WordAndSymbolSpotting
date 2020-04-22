# * this is a single runner file. I thought it would be easier to combine our work this way.


import sys
from dataLoader import load_data
from evaluateAlgorithm import evaluate
from extractDescriptors import extract_descriptors

# check that the user has included enough arguments
if len(sys.argv) < 2:
    print("Usage:\n\tpython3 dataLoader.py path/to/data [optional: randomize]")
    exit(0)

dataPath = sys.argv[1]

if len(sys.argv) > 2:
    randomize = True
else:
    randomize = False


# --------------------------------------------
# Load Data
# --------------------------------------------
print("Loading Images...")
queryImages, testImages, trainImages, testDict, trainDict = load_data(dataPath,randomize)
print("Read " + str(len(queryImages)) + " query images, " + str(len(trainImages)) + " training images, and " + str(len(testImages)) + " testing images\n")


# --------------------------------------------
# Compute Descriptors
# - SIFT: https://docs.opencv.org/master/da/df5/tutorial_py_sift_intro.html
# --------------------------------------------

# *** seemed strange to me to calculate the keypoints with harris-laplace if we are using sift. I just implemented sift for now but we can change it later if needed.

print("Computing keypoints and descriptors...")
queryKeypoints, queryDescriptors = extract_descriptors(queryImages)
trainKeypoints, trainDescriptors = extract_descriptors(trainImages)
testKeypoints, testDescriptors = extract_descriptors(testImages)


# --------------------------------------------
# Build Hash Table --> Geena
# --------------------------------------------
# - create hash table
# - place keypoints for text/train into hash table based on descriptors
# - place into 2 closest indices to avoid boundary effects (like paper)


# --------------------------------------------
# Retrieve Descriptors using query descriptors
# --------------------------------------------
# - pull similar descriptors to the query from the hash table


# --------------------------------------------
# Build proximity graph and find spatial organization (Hough transform)
# - hough: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
# --------------------------------------------



# --------------------------------------------
# Voting Mechanism
# --------------------------------------------



# --------------------------------------------
# Evaluation Algorithm
# --------------------------------------------

