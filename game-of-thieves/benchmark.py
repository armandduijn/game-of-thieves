from abc import ABC, abstractmethod

import networkx as nx
import matplotlib.pyplot as plt
import timeit
import GOT
import library


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


class AbstractAlgorithm(ABC):
    def __init__(self, G):
        self.network = G

    @abstractmethod
    def execute(self, **kwargs):
        """
        Executes the algorithm

        :param kwargs: Arguments
        :return:
        """
        pass

    def time(self, number=5, **kwargs):
        """
        Times the running time of the algorithm

        :param number: Number of times
        :param kwargs: Arguments for the algorithm
        :return: Average running time in seconds
        """
        seconds = timeit.timeit(stmt=lambda: self.execute(**kwargs), number=number)

        return seconds/number


class BaseImplementation(AbstractAlgorithm):
    def execute(self, **kwargs):
        return GOT.ComputeCentrality(G=self.network, **kwargs)


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

algorithm = BaseImplementation(G)
seconds = algorithm.time(number=iterations, **settings)

print('Average time ({} iterations): {:0.4f}s'.format(iterations, seconds))
