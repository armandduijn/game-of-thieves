from algorithms import BaseImplementation, TestImplementation

import library
import matplotlib.pyplot as plt
import networkx as nx


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
    'num_thiefs': 3,      # Number of thieves per node
    'num_vdiamonds': 10,  # Number of vdiamonds per node
    'num_epochs': 1000,   # Number of epochs
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
