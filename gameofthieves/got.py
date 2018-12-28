from thief import Thief

import networkx as nx
import numpy as np
import random


def compute_centrality(G, num_thiefs, num_vdiamonds, num_epochs, seed=0):
    random.seed(seed)

    num_nodes = nx.number_of_nodes(G)
    num_edges = G.number_of_edges()

    # Initialize GOT parameters on the graph
    G = initialize_graph(G, num_vdiamonds)

    # Initialize a list with thieves
    thiefs = []

    # TODO: Add description
    edges = np.zeros((num_edges, 2))
    i = 0
    for edge in G.edges(data=True):
        edges[i] = np.asarray([edge[0], edge[1]])
        i += 1

    # Run GOT for a specific number of epochs
    k = 0
    while k < num_epochs:
        k += 1

        # Make a move for each thief
        for thief in thiefs:
            thief.move(G, k)

        # In the first epoch create the thieves for each node
        if k == 1:
            for i in range(num_nodes):
                if G.neighbors(i):
                    for j in range(num_thiefs):
                        thiefs.append(Thief(i))


def compute_centrality_parallel(G, num_thiefs, num_vdiamonds, num_epochs, seed=0):
    return True


def initialize_graph(G, num_vdiamonds):
    num_nodes = nx.number_of_nodes(G)

    # Initialize the amount of vdiamonds per node
    for i in range(num_nodes):
        G.node[i]['vdiamonds'] = num_vdiamonds

    return G
