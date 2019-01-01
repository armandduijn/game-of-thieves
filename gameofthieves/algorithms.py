from abc import ABC, abstractmethod

import got
import timeit
import movement_serial
import movement_parallel
import networkx as nx


class AbstractAlgorithm(ABC):
    def __init__(self, G):
        self.G = G

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
        del kwargs['num_vdiamonds']
        del kwargs['seed']
        del kwargs['processors']

        # return got.compute_centrality(G=self.G, **kwargs)
        return movement_serial.main(n=nx.number_of_nodes(self.G), **kwargs)


class TestImplementation(AbstractAlgorithm):
    def execute(self, **kwargs):
        del kwargs['num_vdiamonds']
        del kwargs['seed']

        # return got.compute_centrality_parallel(G=self.G, **kwargs)
        return movement_parallel.main(n=nx.number_of_nodes(self.G), **kwargs)
