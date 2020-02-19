"""
1. load data from a location provided by a user
2. load data into "train" and "test" sets
3. load any labelling or ground-truth that corresponds correctly with the associate data sample
4. make the retrieve data and ground-truth iterable
5. have the option to randomize the data
"""

import sys, cv2, numpy, os, random

if len(sys.argv) < 2:
    print("Usage:\n\tpython3 dataLoader.py path/to/data [optional: randomize")
    exit(0)

data_path = sys.argv[1]

if not(data_path[-1] == '/'):
    data_path = data_path + '/'

if len(sys.argv) > 2:
    randomize = True
else:
    randomize = False

query_images = os.listdir(data_path+"queries/")

training_data = os.listdir(data_path+"train/data/")
training_labels = os.listdir(data_path+"train/label/")
training_indices = [x for x in range(0,len(training_data))]

testing_data = os.listdir(data_path+"test/data/")
testing_labels = os.listdir(data_path+"test/label/")
testing_indices = [x for x in range(0,len(testing_data))]

if randomize:
    random.shuffle(training_indices)
    random.shuffle(testing_indices)

for idx in training_indices:
    # result = awesome_alg(query_images,training_data[idx])
    # metrics = evaluate(training_labels[idx],result)
    None

for idx in testing_indices:
    # result = awesome_alg(query_images,testing_data[idx])
    # metrics = evaluate(testing_labels[idx],result)
    None
