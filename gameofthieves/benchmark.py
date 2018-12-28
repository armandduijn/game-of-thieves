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


def plotResults(x, results):
    plt.figure(figsize=(5, 5))

    for key, values in results.items():
        plt.plot(x, values, marker='o', label=key)

    plt.legend()
    plt.xlabel('Nodes')
    plt.ylabel('Average Duration (s)')
    plt.savefig('duration.pdf')


# Perform GoT algorithm
settings = {
    'num_thiefs': 3,      # Number of thieves per node
    'num_vdiamonds': 10,  # Number of vdiamonds per node
    'num_epochs': 1000,   # Number of epochs
    'seed': 0,            # Randomness seed
}

iterations = 3  # Number of times to run the algorithm

search_space = {
    'n': [10, 20, 50]
}

results = {}
for n in search_space.get('n'):
    G = library.generateNetwork(N=n, cnType='scale-free', weighted=True, seed=settings.get('seed'))

    implementations = [
        BaseImplementation(G),
        TestImplementation(G),
    ]

    for implementation in implementations:
        name = implementation.__class__.__name__

        print('Running %s with n=%d...' % (name, n))

        if not results.get(name):
            results[name] = []

        results[name].append(implementation.time(number=iterations, **settings))

plotResults(search_space.get('n'), results)

print(results)
