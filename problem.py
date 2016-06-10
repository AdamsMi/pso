from math import cos, pi

import math
from numpy.random import random
import config


class StoppingCriterion(object):
    """
    Stopping criterion for the optimization algorithm. Right now there are
    two criterion types available:
        * `nr_steps`, meaning that the solver will run for a given number of steps and then return the
           the best solution it found
        * `target_fit`, meaning that the solver will run until the best fitness is smaller than a certain value.

    If you want a default criterion, call `StoppingCriterion.default()`.
    """
    def __init__(self, method, value, max_steps=1000):
        """
        Class constructor.
        :param method: either `nr_steps` or `target_fitness`
        :param value: value of the criterion
        :param max: hard limit on steps with the target_fitness criterion
        """
        if method != 'nr_steps' and method != 'target_fitness':
            print '[ERROR] Method has to be either "nr_steps" or "target_fitness"'
            return

        self.method = method
        self.criterion_value = value
        self.max = max_steps

    def is_met(self, step_nr, fitness):
        """
        Tests whether this stopping criterion is met.
        :param step_nr: Step number in case the criterion is step-based
        :param fitness: Fitness, in case the criterion is target-fitness basded
        :return: boolean -- is the criterion met?
        """
        if self.method == 'nr_steps':
            return self.criterion_value == step_nr

        if self.method == 'target_fitness':
            return fitness <= self.criterion_value or step_nr > self.max

    def is_step_criterion(self):
        return self.method == 'nr_steps'

    def is_target_criterion(self):
        return self.method == 'target_fitness'

    @staticmethod
    def default():
        """
        Default stopping criterion: number-of-steps-based, with the number
        of steps specified by the `config.nr_steps` field.
        :return: Default StoppingCriterion object.
        """
        return StoppingCriterion('nr_steps', config.nr_steps)


class ObjFunc(object):
    """
    Objective function for the optimization problem.
    It actually contains only two fields: the function itself and the dimensionality of the problem.
    """
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


def ackley_func(currPos):
    a = 20
    b = 0.2
    c = 2 * math.pi
    d = float(len(currPos))

    sum_of_squares = sum([x * x for x in currPos])
    sum_of_coss = sum([math.cos(c * x) for x in currPos])

    A = (-b) * math.sqrt(sum_of_squares / d)
    B = sum_of_coss / d

    return (-a) * math.exp(A) - math.exp(B) + a + math.exp(1.0)


def rosenbrock_func(currPos):
    sum = 0.0
    d = len(currPos)

    for i in xrange(d-1):
        sum += ((1 - currPos[i]**2) + 100 * (currPos[i + 1] - currPos[i]**2) ** 2)

    return sum

def reverse_sign(obj_function):
    return ObjFunc(obj_function.dim, lambda x: -(obj_function.func(x)))