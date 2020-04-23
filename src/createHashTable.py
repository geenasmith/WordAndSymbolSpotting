"""
Description:  Creates a hash table and inserts a dictionary for each keypoint using the hash of the descriptor.
Inputs:       "hashSize" which is the number of indices in the hash table, "kps" which is a list of keypoint objects
              for each image, and "descs" which is a list of descriptors for each keypoint within an image
Returns:      "hashTable" which is the hash table list with dictionaries for each keypoint at the indices.
"""

def create_obj(kp,des,idx):
    # add the keypoint obj, descriptor, and image index to a dictionary.
    # dictionary will be what is added to the hash table

    dictObj = {}
    dictObj["xy"] = kp.pt
    dictObj["size"] = kp.size
    dictObj["angle"] = kp.angle
    dictObj["response"] = kp.response
    dictObj["octave"] = kp.octave
    dictObj["des"] = des
    dictObj["idx"] = idx

    return dictObj


def create_hash(hashSize,kps,descs):

    # create empty hash table
    hashTable = [[] for _ in range(0,hashSize)]

    # loop through each keypoint/descriptor, hash, and add to table
    for img in range(0,len(kps)):  # loop through each image
        for n in range(0,len(kps[img])):  # loop through each keypoint/descriptor

            dictObj = create_obj(kps[img][n],descs[img][n],img)

            hashVal = hash(tuple(descs[img][n])) % hashSize
            hashTable[hashVal].append(dictObj)  #** only adding to a single index for now

    return hashTable
