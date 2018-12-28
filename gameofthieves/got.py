from thief import Thief

import networkx as nx
import numpy as np
import random

from multiprocessing import Pool, Lock

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

    lock = Lock()

    # Run GOT for a specific number of epochs
    k = 0
    while k < num_epochs:
        k += 1

        # Make a move for each thief
        for thief in thiefs:
            thief.move(G, lock)

        # In the first epoch create the thieves for each node
        if k == 1:
            for i in range(num_nodes):
                if G.neighbors(i):
                    for j in range(num_thiefs):
                        thiefs.append(Thief(i))


def compute_centrality_parallel(G, num_thiefs, num_vdiamonds, num_epochs, seed=0):
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

    lock = Lock()
    pool = Pool(processes=2, initializer=initialize_pool, initargs=(lock,))

    k = 0
    while k < num_epochs:
        k += 1

        # Move the thieves
        pool.starmap(walk, [(G, thief) for thief in thiefs])

        # In the first epoch create the thieves for each node
        if k == 1:
            for i in range(num_nodes):
                if G.neighbors(i):
                    for j in range(num_thiefs):
                        thiefs.append(Thief(i))


def initialize_pool(l):
    global lock
    lock = l

def walk(G, thief):
    thief.move(G, lock)

# def __initialize_threads(num_threads, *args):
#
#     for _ in range(num_threads):
#         worker = Thread(target=__manager, args=args)
#
#         worker.setDaemon(True)
#         worker.start()


# def __manager(queue, G, thiefs):
#
#     while True:
#         thief = thiefs[queue.get()]
#         thief.move(G)
#
#         queue.task_done()


def initialize_graph(G, num_vdiamonds):
    num_nodes = nx.number_of_nodes(G)

    # Initialize the amount of vdiamonds per node
    for i in range(num_nodes):
        G.node[i]['vdiamonds'] = num_vdiamonds

    # Initialize the thieves passes per edge
    for edge in G.edges():
        G.add_edge(edge[0], edge[1], passes=0)

    return G
