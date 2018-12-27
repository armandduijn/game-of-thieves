import networkx as nx
import matplotlib.pyplot as plt
import library

from algorithms import BaseImplementation, TestImplementation


def visualize(G, filename):
    """
    Generates a visualization of the graph

    :param G: NetworkX graph object
    :param filename: Filename of the PDF
    :return: void
    """
    plt.figure(figsize=(20, 20))

    positions = nx.spring_layout(G)
    nx.draw_networkx_nodes(G=G, pos=positions, node_size=5)
    nx.draw_networkx_edges(G=G, pos=positions, alpha=0.3)

    plt.axis('off')
    plt.savefig(filename + '.pdf')


G = library.generateNetwork(N=10, cnType='scale-free', weighted=True, seed=0)

# Export a visualization to understand what the GoT is calculating on
visualize(G, 'graph')

# Perform GoT algorithm
settings = {
    'noThiefs': 3,      # Number of thieves per node
    'noVDiamonds': 10,  # Number of vdiamonds per node
    'noEpochs': 1000,   # Number of epochs
}

iterations = 3  # Number of times to run the algorithm

implementations = [
    BaseImplementation(G),
    TestImplementation(G),
]

results = {}
for implementation in implementations:
    name = implementation.__class__.__name__

    print('Running %s...' % name)

    results[name] = implementation.time(number=iterations, **settings)

print(results)
