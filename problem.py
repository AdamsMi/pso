from math import cos, pi
from numpy.random import random


class Point(object):
    def __init__(self, dim, coord_min, coord_max):
        self.position = [(coord_max - coord_min) * random() + coord_min for _ in xrange(dim)]
        self.currFitness = eval_fitness(self.position)

    def __str__(self):
        return str(self.position) + "\nfitness: " + str(self.currFitness)


def rastrigin_func(currPos):
    fitness = 10 * len(currPos)
    for el in currPos:
        fitness += el ** 2 - (10 * cos(2 * pi * el))
    return fitness


def eval_fitness(pos):
    return rastrigin_func(pos)
