
import sys
from dataLoader import load_data
from evaluateAlgorithm import evaluate
from extractDescriptors import extract_descriptors
from createHashTable import create_hash
from proximityGraph import create_prox_graphs
from generalizedHough import generalized_hough, compute_hC

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
queryImages, dataImages, dataDict = load_data(dataPath, randomize)
print("Read " + str(len(queryImages)) + " query images, and " + str(len(dataImages)) + " data images\n")


# --------------------------------------------
# Compute Descriptors
# - SIFT: https://docs.opencv.org/master/da/df5/tutorial_py_sift_intro.html
# --------------------------------------------
# *** seemed strange to me to calculate the keypoints with harris-laplace if we are using sift. I just implemented sift for now but we can change it later if needed.
print("Computing keypoints and descriptors...\n")
queryKeypoints, queryDescriptors = extract_descriptors(queryImages)
dataKeypoints, dataDescriptors = extract_descriptors(dataImages)


# --------------------------------------------
# Build Hash Table
# --------------------------------------------
print("Building hash table...\n")
hashSize = int(min(map(len, dataKeypoints)) * 0.75)  # currently 70% of the min number of descriptors. Paper used a value less than # of descriptors
hashTable = create_hash(hashSize, dataKeypoints, dataDescriptors)


# --------------------------------------------
# Retrieve Descriptors using query descriptors
# --------------------------------------------
# - pull similar descriptors to the query from the hash table
# print("Extracting similar descriptors...\n")
# Moved into generalized_hough()
# similarDescriptors = []

# # For each query image and descriptor
# for img in range(len(queryDescriptors)):
#     similar_to_query = []
#     for desc in range(0, len(queryDescriptors[img])):
#         # Get all similar descriptors to this descriptor
#         hash_value = hash(tuple(queryDescriptors[img][n])) % hashSize
#         similar_to_query.extend(hashTable[hash_value])
#     # Add to list for each query image
#     similarDescriptors.append(similar_to_query)

# --------------------------------------------
# Build proximity graph and find spatial organization (Hough transform)
# - hough: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
# --------------------------------------------
print("Building proximity graphs...\n")
queryGraphs = create_prox_graphs(queryKeypoints, queryDescriptors)
# dataGraphs = create_prox_graphs(dataKeypoints)

# --------------------------------------------
# Voting Mechanism
# --------------------------------------------
# Get the shape of all query images for hC computing
dataImgShapes = [img.shape for img in dataImages]

print("Starting generalized Hough transform...\n")
generalized_hough(queryGraphs, dataKeypoints, dataImgShapes, hashTable, hashSize)



# --------------------------------------------
# Evaluation Algorithm
# --------------------------------------------

