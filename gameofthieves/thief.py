import numpy as np
import random


class Thief:
    def __init__(self, origin):
        self.origin = origin
        self.position = origin
        self.diamond = 0
        self.path = []

    def move(self, G, lock):
        if self.diamond == 0:
            self.search(G)

            if self.position != self.origin:
                self.take_diamond(G, lock)
        else:
            self.back(G, lock)

    def search(self, G):
        neighboursList = G[self.position]
        moveProb=np.zeros(len(neighboursList))
        sumWeights=0

        for neighbour in neighboursList:
            sumWeights+=G.edges[self.position,neighbour]['value']

        i=0
        for neighbour in neighboursList:
            moveProb[i]=(float)(G.edges[self.position,neighbour]['value'])/sumWeights
            i+=1

        rdProb=random.random()
        sumProb=0
        i = 0

        for neighbour in neighboursList:
            sumProb+=moveProb[i]
            if (sumProb>=rdProb):
                moveTo=neighbour
                break
            i += 1
        try:
            index=self.path.index(moveTo)
        except ValueError:
            index=-1

        if (index>-1):
            for i in range(index+1,len(self.path)):
                del self.path[-1]

        self.path.append(self.position)
        self.position=moveTo
        if (self.origin==self.position):
            self.path=[]

    def take_diamond(self, G, lock):
        lock.acquire()

        # Pick-up a vdiamond if the current node has vdiamonds
        if G.node[self.position]['vdiamonds'] > 0:
            G.node[self.position]['vdiamonds'] -= 1

            self.diamond = 1

        lock.release()

    def back(self, G, lock):
        lock.acquire()

        # Update amount of passes on edge
        current_edge = G.get_edge_data(self.position, self.path[-1])
        thiefs_passes = current_edge['passes'] + 1

        G.add_edge(self.position, self.path[-1], passes=thiefs_passes)

        # Move the thief to its previously visited node
        self.position = self.path[-1]
        del self.path[-1]

        # Update origin node if the thief has returned
        if self.position == self.origin:
            self.path = []
            self.diamond = 0
            self.position = self.origin

            G.node[self.position]['vdiamonds'] += 1

        lock.release()
