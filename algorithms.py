from abc import ABC, abstractmethod

import timeit
import GOT


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


class TestImplementation(AbstractAlgorithm):
    def execute(self, **kwargs):
        return True
