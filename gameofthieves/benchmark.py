from algorithms import BaseImplementation, TestImplementation

import library
import matplotlib.pyplot as plt
import networkx as nx
import logging
import json
import hashlib
import multiprocessing

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


def plot_results(x, settings, results):
    # Generate a unique filename with the used settings
    settings_hash = hashlib.md5(json.dumps(settings).encode('utf-8')).hexdigest()
    filename = 'duration_%s.pdf' % settings_hash

    # Generate a string of the used settings
    parameters = []
    for key, value in settings.items():
        parameters.append('%s=%s' % (key, value))

    parameters = ', '.join(parameters)

    # Generate graph
    plt.figure(figsize=(5, 5))

    for key, values in results.items():
        plt.plot(x, values, marker='o', label=key)

    plt.suptitle('Average Duration of Implementations')
    plt.title(parameters, fontsize=6)
    plt.legend()
    plt.xlabel('Nodes')
    plt.ylabel('Average Duration (s)')
    plt.savefig(filename)

    return filename


# Setup benchmark

logging.basicConfig(level=logging.INFO)

iterations = 3  # Run each algorithm 3 times
processors = multiprocessing.cpu_count()  # Use all available processors

# Perform GoT algorithm
settings = {
    'num_thiefs': 3,          # Number of thieves per node
    'num_vdiamonds': 10,      # Number of vdiamonds per node
    'num_epochs': 1000,       # Number of epochs
    'seed': 0,                # Randomness seed
    'processors': processors  # Number of CPU processors to use
}

search_space = {
    'n': [10, 20, 50]
}

results = {}
for n in search_space.get('n'):
    logging.info('Generating a network with %d nodes' % n)

    G = library.generateNetwork(N=n, cnType='scale-free', weighted=True, seed=settings.get('seed'))

    implementations = [
        BaseImplementation(G),
        TestImplementation(G),
    ]

    for implementation in implementations:
        name = implementation.__class__.__name__

        logging.info('Running %s' % name)

        if not results.get(name):
            results[name] = []

        results[name].append(implementation.time(number=iterations, **settings))

logging.info('Exporting results')

path = plot_results(search_space.get('n'), settings, results)

logging.info("Results stored in '%s'" % path)

print(results)
