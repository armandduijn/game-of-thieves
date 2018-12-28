import numpy as np
import random


class Thief:
    def __init__(self, origin):
        self.origin = origin
        self.position = origin
        self.diamond = 0
        self.path = []

    def move(self, G):
        if self.diamond == 0:
            self.search(G)

            if self.position != self.origin:
                self.take_diamond(G)
        else:
            self.back(G)

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

    def take_diamond(self, G):
        pass

    def back(self, G):
        pass
