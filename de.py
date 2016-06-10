from copy import copy

import numpy.random as npr
import matplotlib.pyplot as plt

from problem import rastrigin_func, Point, StoppingCriterion
import config

default_params = {'CR': 0.9, 'F': 0.5}
counter = 0

# helper function for random indices:
def randint(high):
    return npr.randint(0, high)


# pick three indices different from each other and from x:
def pick_3_diff(population, pop_s, i):
    a_i = randint(pop_s)
    while a_i == i:
        a_i = randint(pop_s)

    b_i = randint(pop_s)
    while b_i == i or b_i == a_i:
        b_i = randint(pop_s)

    c_i = randint(pop_s)
    while c_i == i or c_i == a_i or c_i == b_i:
        c_i = randint(pop_s)

    a = population[a_i]
    b = population[b_i]
    c = population[c_i]

    return a, b, c


# run a single step of the algorithm:
def run_step(fit_func, population, dimensionality, population_size, coord_min, coord_max, CR, F):
    global counter
    # for every agent in the population:
    for idx in xrange(population_size):
        x = population[idx]
        # pick 3 different agents randomly:
        a, b, c = pick_3_diff(population, population_size, x)

        R = randint(dimensionality)

        # new, candidate position:
        y = Point(dimensionality, coord_min, coord_max)
        for i in xrange(dimensionality):
            r_i = npr.random()
            if r_i < CR or i == R:
                y.position[i] = a.position[i] + F * (b.position[i] - c.position[i])
            else:
                y.position[i] = x.position[i]

        y.currFitness = fit_func(y.position)
        counter += 1

        if y.currFitness < x.currFitness:
            population[idx] = y


# calculate the best fitness so far:
def get_best_fit(population):
    b_part = min(population, key=lambda p: p.currFitness)
    b_fit = b_part.currFitness
    b_pos = b_part.position[:]
    return b_part, b_fit, b_pos


# run the differential evolution algorithm
# note: 0 < CR < 1, 1 < F < 2
def solve(fit_func, dimensionality, population_size, interval, stopping_criterion,
          method_params, verbose=False):
    CR = method_params['CR'] if method_params is not None and 'CR' in method_params else default_params['CR']
    F = method_params['F'] if method_params is not None and 'F' in method_params else default_params['F']

    global counter

    # initialize the population:
    population = []
    coord_min, coord_max = interval
    for i in xrange(population_size):
        p = Point(dimensionality, coord_min, coord_max)
        p.currFitness = fit_func(p.position)
        population.append(p)

    prog = []
    best_particle, best_fitness, best_pos = get_best_fit(population)
    prog.append(best_fitness)

    step_nr = 0
    # for step in xrange(nr_steps):

    while not stopping_criterion.is_met(step_nr, best_fitness):
        step_nr += 1
        run_step(fit_func, population, dimensionality, population_size, coord_min, coord_max, CR, F)
        bp, bf, bps = get_best_fit(population)
        if bf < best_fitness:
            best_particle, best_fitness, best_pos = bp, bf, bps

        prog.append(best_fitness)

    if verbose:
        print "Best fitness: {0}".format(best_fitness)

    return prog, best_pos


def run_de(fit_func, dimensionality, population_size, interval, stopping_criterion,
           method_params, chart=False, verbose=False):
    """
    Runs the optimization process using the Differential Evolution method (DE).
    :param fit_func: Function that evaluates the fitness of a given solution.
    :param dimensionality: dimensionality of the problem (i.e. domain of the fit_func)
    :param population_size: Size of the swarm
    :param interval: interval on which the function should be optimized will be a square:
    interval^dim (^ meaning the power using cartesian product).
    :param stopping_criterion: object of class `problem.StoppingCriterion`
    :param method_params: dict with parameters for the method. For Differential evolution the parameters are:
    `CR` and `F`.
    :param chart: boolean -- should the results be plotted?
    :param verbose: boolean -- should the method print additional info?
    :return: depending on the stopping criterion either best solution, or number of steps
    required to achieve this solution
    """
    global counter
    counter = 0
    if verbose:
        print "SIZE OF POPULATION: ", population_size

    progress, solution = solve(fit_func, dimensionality, population_size,
                               interval, stopping_criterion, method_params)
    if chart:
        plt.plot(progress)
        plt.show()

    if stopping_criterion.is_step_criterion():
        return solution

    if stopping_criterion.is_target_criterion():
        return counter

    # default case:
    return solution


def param_fit(obj_function,
              population_size=config.population_size,
              interval=(config.coord_min, config.coord_max)):
    """
        Tries to find the best parameters for DE.
        :param obj_function: function to be minimized
        :param population_size: size of the population to use during the algorithm
        :param interval: interval on which to optimize the function
        :return: dictionary with best parameters
        """
    CRs = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    Fs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    stopping_criterion = StoppingCriterion.default()

    params = {}
    best_params = {}
    best_fit = 10000000

    for CR in CRs:
        for F in Fs:
            params['CR'] = CR
            params['F'] = F

            fit = run_de(fit_func=obj_function.func,
                         dimensionality=obj_function.dim,
                         population_size=population_size,
                         interval=interval,
                         stopping_criterion=stopping_criterion,
                         method_params=params)

            if fit > best_fit:
                best_fit = fit
                best_params = copy(params)

    return best_params


if __name__ == '__main__':
    run_de(fit_func=rastrigin_func,
           dimensionality=config.dimensionality,
           population_size=config.population_size,
           interval=(config.coord_min, config.coord_max),
           stopping_criterion=StoppingCriterion.default(),
           method_params={'CR': 0.9, 'F': 0.5},
           chart=True)
