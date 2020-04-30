import numpy as np
import networkx as nx
import cv2
from proximityGraph import create_prox_graph_from_point


def generalized_hough(queryGraphs, dataKeypoints, dataImgShapes, hashTable, hashSize):
    """
    Computes x,y coordinates of models similar to the given query using a generalized Hough transform approach.

    :param queryGraphs:
    :param dataKeypoints:
    :param dataImgShapes:
    :param hashTable:
    :param hashSize:
    :return:
    """

    # Compute the hC vectors for each query kp pair
    compute_hC(queryGraphs, dataImgShapes)

    # Initialize a set of graphs to hold the prox graphs of each data image. These are shared to reduce computations.
    dataGraphs = []
    for img in range(len(dataImgShapes)):
        data_graph = nx.Graph()
        # naming convention for data nodes is the tuple (pt, size, angle) for easy retrieval
        for kp in dataKeypoints[img]:
            data_graph.add_node((kp.pt, kp.size, kp.angle), kp=kp)
        dataGraphs.append(data_graph)

    # For each query image
    for img in range(len(queryGraphs)):
        __generalized_hough__(queryGraphs[img], dataGraphs, dataImgShapes, hashTable, hashSize)



def __generalized_hough__(queryGraph, dataGraphs, dataImgShapes, hashTable, hashSize):
    """
    Private function used by generalized_hough for a single query image.

    :param queryGraph: The proximity graph of the query image.
    :param dataGraphs: List of proximity graphs for each data image. Incomplete graphs will be completed as necessary.
    :param dataImageShapes: List of array shapes for each data image.
    :param hashTable: The hash table containing all keypoints.
    :param hashSize: Size of hash.
    :return: A list of (x,y) coordinates for objects similar to the query image in the data images.
    """

    # Initialize heatmaps for each data image
    heatmaps = []
    for img in range(len(dataGraphs)):
        l, w, _ = dataImgShapes[img]
        heatmaps.append(np.zeros((l, w), dtype=np.uint8))

    # For each kp in query
    for kp in list(queryGraph.nodes):
        # Retrieve similar kps to kp from the hash table
        similar_desc = hashTable[hash(tuple(queryGraph.nodes[kp]["desc"])) % hashSize]

        # For each outgoing edge from kp s.t. kp2 > kp
        for kp2 in list(queryGraph.adj[kp]):
            if kp >= kp2:
                continue

            # Retrieve similar kps to kp2 from the hash table
            similar_desc2 = hashTable[hash(tuple(queryGraph.nodes[kp2]["desc"])) % hashSize]

            # For each similar hashed descriptor kp
            for desc in similar_desc:
                # Grab the dataGraph corresponding to the image where the descriptor originates
                data_graph = dataGraphs[desc["idx"]]
                node = get_node_name_from_desc(desc)

                # If edges have not been added for this node
                if data_graph.degree[node] == 0:
                    # Add edges to the k closest nodes
                    create_prox_graph_from_point(data_graph, node)

                # For each similar hashed descriptor kp2
                for desc2 in similar_desc2:
                    target_node = get_node_name_from_desc(desc2)

                    # If desc and desc2 are in the same image AND are connected by an edge
                    if desc["idx"] == desc2["idx"] and data_graph.has_edge(node, target_node):

                        if target_node is node:
                            continue
                        # Get vector (xi,xj)
                        xi = np.asarray(data_graph.nodes[node]["kp"].pt)
                        xj = np.asarray(data_graph.nodes[target_node]["kp"].pt)

                        # If xi and xj are on the same point
                        if np.array_equal(xi, xj):
                            # # Add the displacement to xi
                            # hC = np.add(xi, queryGraph.edges[kp, kp2]["displacement"])
                            xj = np.array([1, 0])

                        # Rotate vector by theta. Not sure if there's a built in function for this
                        theta = queryGraph.edges[kp, kp2]["theta"]
                        x_ij = np.subtract(xj, xi)
                        c, s = np.cos(theta), np.sin(theta)
                        R = np.array(((c, -s), (s, c)))
                        x_ic = np.dot(R, np.transpose(x_ij))

                        # Scale by mag
                        x_ic *= queryGraph.edges[kp, kp2]["mag"]

                        # Add back to xi
                        hC = np.add(xi, x_ic)

                        # Increment point on heatmap
                        heatmap = heatmaps[desc["idx"]]
                        if is_in_bounds(heatmap, hC):
                            heatmap[int(round(hC[0]))][int(round(hC[1]))] += 1

    for heatmap in heatmaps:
        pass
        # cv2.imshow('SIFT', heatmap)
        # cv2.waitKey()


def compute_hC(queryGraphs, dataImgShapes):
    """
    Computes the hypothetical center hC of each keypoint pair in query and returns the angle and magnitude of hC from
    the first point.

    :param queryGraphs: A list of proximity graphs corresponding to each query image
    :param dataImgShapes: A list of query image shapes [l,w,3]
    :return: List of (angle, magnitude) pairs for each kp pair
    """
    # calculate the center point of each query image
    centerpoints = []
    for shape in dataImgShapes:
        centerpoints.append((shape[0]/2, shape[1]/2))

    # loop through each image
    for img in range(len(queryGraphs)):
        # loop through each node
        for i in range(len(queryGraphs[img].nodes)):
            # for each node connected to i
            for j in queryGraphs[img].adj[i]:
                # Only continue if i < j
                if i >= j:
                    continue

                # Get vectors (xi,xj) and (xi,centerpoint)
                xi = np.asarray(queryGraphs[img].nodes[i]["kp"].pt)
                xj = np.asarray(queryGraphs[img].nodes[j]["kp"].pt)
                x_ic = np.subtract(centerpoints[img], xi)

                # If xi and xj are the same point
                if np.array_equal(xi, xj):
                    # queryGraphs[img].edges[i, j]['displacement'] = x_ic
                    # continue
                    xj = np.array([1, 0])

                # Get scale value of norm(x_ic) as compared to norm(x_ij)
                x_ij = np.subtract(xj, xi)
                x_ij_n = np.linalg.norm(x_ij)
                x_ic_n = np.linalg.norm(x_ic)

                mag = x_ic_n / x_ij_n

                # Convert to unit vector
                x_ij_u = x_ij / x_ij_n
                x_ic_u = x_ic / x_ic_n

                # Calculate angle theta from vector (xi,xj) to (xi,centerpoint)
                theta = np.arccos(np.clip(np.dot(x_ij_u, x_ic_u), -1.0, 1.0))

                # Add theta and scale to the edge (xi, xj)
                queryGraphs[img].edges[i, j]['displacement'] = 0
                queryGraphs[img].edges[i, j]['theta'] = theta
                queryGraphs[img].edges[i, j]['mag'] = mag


def get_node_name_from_desc(desc):
    out = (desc["xy"], desc["size"], desc["angle"])
    return out


def is_in_bounds(array, point):
    x, y = int(round(point[0])), int(round(point[1]))
    max_x, max_y = array.shape
    return 0 <= x < max_x and 0 <= y < max_y
