import networkx as nx
import math
import matplotlib.pyplot as plt
import numpy as np


def create_prox_graphs(kps, descs, k=5):
    """
    Function which creates a proximity graph given a set of points.

    :param kps: list containing sets of keypoints
    :param descs: list containing sets of descriptors
    :param k: number of neighbor edges to add out of each point
    :return: list containing a proximity graph for each set of points
    """
    """
    proximity graph:
        create 2 graphs G(O) and Gprox(O)
        G(O):
            for each point xi:
                for each point xj | i <= j:
                    add edge (xi, xj)
                    calculate Eulidean distance and add as edge weight
        Gprox(O):
            for each point xi:
                add the k smallest weights from G(O)
	"""
    prox_graphs = []

    # loop through each image
    for img in range(len(kps)):
        g_data = nx.Graph()
        g_prox = nx.Graph()

        # Create a fully connected graph g_data. Each node contains its keypoint and descriptor.
        for i in range(len(kps[img])):
            g_data.add_node(i, kp=kps[img][i], desc=descs[img][i])
            g_prox.add_node(i, kp=kps[img][i], desc=descs[img][i])

        # add Euclidean distance as weights
        for i in range(len(kps[img])):
            for j in range(i+1, len(kps[img])):
                g_data.add_edge(i, j, weight=distance_2d(g_data.nodes[i]["kp"].pt, g_data.nodes[j]["kp"].pt))

        # add all k smallest edges from each node to g_prox
        for i in range(len(kps[img])):
            # get a list of outgoing edges sorted by weight
            sorted_nodes = sorted(g_data.adj[i].items(), key=lambda x: (x[1]["weight"], x[0]))

            # add the first k edges to the g_prox graph
            for _k in range(k):
                g_prox.add_edge(i, sorted_nodes[_k][0], weight=sorted_nodes[_k][1]["weight"])

        # append g_prox to list
        prox_graphs.append(g_prox)

        # draw g_prox for debugging
        # nx.draw(g_prox, with_labels=True, font_weight='bold')
        # plt.show()

    return prox_graphs


def create_prox_graph_from_point(g, node, k=5):
    temp_g = nx.Graph()
    temp_g.add_nodes_from(g)
    # Fully connect node with all other nodes with weight as Euclidean distance.
    for target_node in list(temp_g.nodes):
        if node == target_node:
            continue
        temp_g.add_edge(node,
                        target_node,
                        weight=distance_2d(g.nodes[node]["kp"].pt, g.nodes[target_node]["kp"].pt)
                        )

    # get a list of outgoing edges sorted by weight
    sorted_nodes = sorted(temp_g.adj[node].items(), key=lambda x: (x[1]["weight"], x[0]))

    # add the first k edges to the g_prox graph
    for _k in range(k):
        g.add_edge(node, sorted_nodes[_k][0], weight=sorted_nodes[_k][1]["weight"])


def distance_2d(pt1, pt2):
    return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)