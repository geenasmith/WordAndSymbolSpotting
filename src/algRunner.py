# * this is a single runner file. I thought it would be easier to combine our work this way.


import sys
from dataLoader import load_data
from evaluateAlgorithm import evaluate

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
# Extract Keypoints --> Geena
# - harris-laplace: https://docs.opencv.org/3.4/d4/d7d/tutorial_harris_detector.html
# --------------------------------------------


# --------------------------------------------
# Compute Descriptors --> Geena
# - SIFT: https://docs.opencv.org/master/da/df5/tutorial_py_sift_intro.html
# --------------------------------------------


# index scheme/hash table

# retrieve descriptors

# spatial organization (Hough transform)
# - hough: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html

# voting mechanism

# evaluation alg