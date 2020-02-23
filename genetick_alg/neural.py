import numpy as np
import random
import math
from copy import deepcopy
def rand01():
    return random.uniform(0,1)


class Network(object):
    def __init__(self,layers=None,weights=None):
        if layers is None:
            self.height = len(weights) + 1
            self.weights = weights
            self.layers = [len(self.weights[0])]
            for i in range(self.height-1):
                self.layers.append(len(weights[i][0]))
        else:
            self.height = len(layers)
            self.layers = layers
            self.init_weights()

    def __str__(self):
        return "Layers: " + ' '.join(list(map(str,self.layers))) + '\n\nWeights:\n'+ '\n\n'.join(['\n'.join([' '.join(list(map(str,i))) for i in j]) for j in self.weights]) +'\n'


    def init_weights(self):

        #Fix me!
        pass

    def train(self,features,targets):
        for i in range(len(targets)):
            result = self.run(features[i])
            self.run_back_propagation(targets[i])


    def run(self,inputs):
        self.values = [inputs]
        for step in range(self.height-1):
            self.values.append([])
            for to in range(self.layers[step+1]):  #I'm not shure but +1 helped)
                arg = 0
                for frm in range(self.layers[step]):
                    # out of range in weights by index to!

                    arg += self.weights[step][frm][to] * self.values[step][frm]
                if step + 2 < self.height:
                    arg = self.activate(arg)
                self.values[step+1].append(arg)
        return arg

    def run_back_propagation(self,etalon):
        old_weights = deepcopy(self.weights)
        deltas = [[] for i in range(self.height)]

        for step in range(self.height-1,0,-1):
            for to in range(self.layers[step]):
                o_j = self.values[step][to]
                if step == self.height-1:
                    delta_j = self.activate(o_j) * (self.activate(o_j) - 1) * (etalon - o_j)
                else:
                    summa = 0
                    for child in range(self.layers[step + 1]):
                        summa += old_weights[step][to][child] * deltas[step + 1][child]
                    delta_j = self.activate(o_j) * (1 - self.activate(o_j)) * summa
                deltas[step].append(delta_j)

                for frm in range(self.layers[step - 1]):
                    self.weights[step - 1][frm][to] += -delta_j * self.values[step - 1][frm]



    def activate(self,x):
        return 1 / (1 + math.exp(-x))
