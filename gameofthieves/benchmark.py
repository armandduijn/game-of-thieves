from algorithms import BaseImplementation, PoolImplementation, BatchImplementation

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
    fig, ax = plt.subplots(nrows=1, ncols=len(results), sharey=True)

    if len(results) == 1:
        ax = [ ax ]

    i = 0
    for network, runs in results.items():
        for implementation, measurements in runs.items():
            ax[i].plot(x, measurements, marker='o', label=implementation)

        ax[i].set_title(network)
        ax[i].set_xlabel('Nodes')
        ax[i].legend()

        i += 1

    plt.suptitle(parameters, fontsize=6)
    fig.text(0.04, 0.5, 'Average Duration (s)', va='center', rotation='vertical')
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
    'type': ['scale-free'],
    'n': [10, 50, 100],
}

results = {}
for network in search_space.get('type'):
    results[network] = {}

    for n in search_space.get('n'):
        logging.info('Generating a %s network with %d nodes' % (network, n))

        G = library.generateNetwork(N=n, cnType=network, weighted=True, seed=settings.get('seed'))

        implementations = [
            BaseImplementation(G),
            PoolImplementation(G),
            BatchImplementation(G),
        ]

        for implementation in implementations:
            name = implementation.__class__.__name__

            logging.info('Running %s' % name)

            if not results[network].get(name):
                results[network][name] = []

            results[network][name].append(implementation.time(number=iterations, **settings))

logging.info('Exporting results')

path = plot_results(search_space.get('n'), settings, results)

logging.info("Results stored in '%s'" % path)

print(results)
