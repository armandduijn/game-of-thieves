from gameofthieves.thief import Thief
from multiprocessing import Lock

import unittest
import networkx as nx
import random


class ThiefTest(unittest.TestCase):
    def setUp(self):
        self.lock = Lock()

        random.seed(0)

    def sample_graph(self, num_vdiamonds):
        G = nx.Graph()  # Undirected graph

        G.add_node(0, vdiamonds=num_vdiamonds)
        G.add_node(1, vdiamonds=num_vdiamonds)
        G.add_node(2, vdiamonds=num_vdiamonds)
        G.add_edge(0, 1, value=1, passes=0)
        G.add_edge(1, 2, value=1, passes=0)
        G.add_edge(2, 1, value=1, passes=0)

        return G

    def test_constructor(self):
        thief = Thief(origin=42)

        self.assertEqual(thief.origin, 42)
        self.assertEqual(thief.position, 42)
        self.assertEqual(thief.diamond, 0)
        self.assertTrue(len(thief.path) == 0)

    def test_move_empty(self):
        G = self.sample_graph(num_vdiamonds=1)

        thief = Thief(origin=0)
        thief.move(G, self.lock)

        self.assertEqual(thief.position, 1)
        self.assertEqual(thief.diamond, 1)
        self.assertListEqual(thief.path, [0])
        self.assertEqual(G.node[0]['vdiamonds'], 1)
        self.assertEqual(G.node[1]['vdiamonds'], 0)
        self.assertEqual(G.edges[0, 1]['passes'], 0)

    def test_move_loaded(self):
        G = self.sample_graph(num_vdiamonds=1)

        thief = Thief(origin=0)
        thief.move(G, self.lock)
        thief.move(G, self.lock)

        self.assertEqual(thief.position, 0)
        self.assertEqual(thief.diamond, 0)
        self.assertEqual(G.node[0]['vdiamonds'], 2)
        self.assertEqual(G.node[1]['vdiamonds'], 0)
        self.assertEqual(G.edges[0, 1]['passes'], 1)

    def test_move_empty_node(self):
        G = self.sample_graph(num_vdiamonds=1)

        G.node[1]['vdiamonds'] = 0  # The second node has already been robbed

        thief = Thief(origin=0)
        thief.move(G, self.lock)
        thief.move(G, self.lock)

        self.assertEqual(thief.position, 2)
        self.assertEqual(thief.diamond, 1)
        self.assertEqual(G.node[0]['vdiamonds'], 1)
        self.assertEqual(G.node[1]['vdiamonds'], 0)
        self.assertEqual(G.node[2]['vdiamonds'], 0)
        self.assertEqual(G.edges[0, 1]['passes'], 0)
        self.assertEqual(G.edges[1, 2]['passes'], 0)

    def test_move_probability(self):
        G = self.sample_graph(num_vdiamonds=1)

        G.add_edge(1, 2, value=2)

        thief = Thief(origin=1)
        thief.move(G, self.lock)  # Move to node 2 because random() = 0.84 > 0.66

        self.assertEqual(thief.position, 2)

    def test_multiple_thiefs_race(self):
        G = self.sample_graph(num_vdiamonds=1)

        thief1 = Thief(origin=0)
        thief2 = Thief(origin=2)

        thief1.move(G, self.lock)  # Thief 1 moves to node 1
        thief2.move(G, self.lock)  # Thief 2 moves to node 1
        thief1.move(G, self.lock)  # Thief 1 moves to its origin

        self.assertEqual(thief1.position, 0)
        self.assertEqual(thief2.position, 1)
        self.assertEqual(thief1.diamond, 0)
        self.assertEqual(thief2.diamond, 0)  # Thief 2 arrived later
        self.assertEqual(G.node[0]['vdiamonds'], 2)  # Thief 1 has brought back a vdiamond
        self.assertEqual(G.node[1]['vdiamonds'], 0)

    def test_multiple_thiefs_origin(self):
        G = self.sample_graph(num_vdiamonds=1)

        thief1 = Thief(origin=0)
        thief2 = Thief(origin=2)

        thief1.move(G, self.lock)  # Thief 1 moves to node 1
        thief2.move(G, self.lock)  # Thief 2 moves to node 1
        thief1.move(G, self.lock)  # Thief 1 moves to its origin
        thief2.move(G, self.lock)  # Thief 1 moves to node 1

        self.assertEqual(thief1.position, 0)
        self.assertEqual(thief2.position, 0)
        self.assertEqual(thief1.diamond, 0)
        self.assertEqual(thief2.diamond, 1)
        self.assertEqual(G.node[0]['vdiamonds'], 1)
        self.assertEqual(G.node[1]['vdiamonds'], 0)
        self.assertEqual(G.edges[0, 1]['passes'], 1)
        self.assertEqual(G.edges[1, 2]['passes'], 0)


if __name__ == '__main__':
    unittest.main()
