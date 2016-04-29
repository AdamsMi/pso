from math import cos, pi
from numpy.random import random


class ObjFunc(object):
    def __init__(self, dim, func):
        self.dim = dim
        self.func = func


class Point(object):
    def __init__(self, dim, coord_min, coord_max):
        self.position = [(coord_max - coord_min) * random() + coord_min for _ in xrange(dim)]
        self.currFitness = None

    def __str__(self):
        return str(self.position) + "\nfitness: " + str(self.currFitness)


def rastrigin_func(currPos):
    fitness = 10 * len(currPos)
    for el in currPos:
        fitness += el ** 2 - (10 * cos(2 * pi * el))
    return fitness


def reverse_sign(obj_function):
    return ObjFunc(obj_function.dim, lambda x: -(obj_function.func(x)))