import numpy.random as npr
import matplotlib.pyplot as plt

from problem import rastrigin_func, Point
import config

default_params = {'CR': 0.9, 'F': 0.5}


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
def run_step(fit_func, population, dimensionality, population_size, coord_min, coord_max, prog, CR, F):
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
        if y.currFitness < x.currFitness:
            prog.append(y.currFitness)
            population[idx] = y
        else:
            prog.append(x.currFitness)


# calculate the best fitness so far:
def get_best_fit(population):
    b_part = min(population, key=lambda p: p.currFitness)
    b_fit = b_part.currFitness
    b_pos = b_part.position[:]
    return b_part, b_fit, b_pos


# run the differential evolution algorithm
# note: 0 < CR < 1, 1 < F < 2
def solve(fit_func, dimensionality, population_size, interval, nr_steps, method_params, verbose=False):
    CR = method_params['CR'] if method_params is not None and 'CR' in method_params else default_params['CR']
    F = method_params['F'] if method_params is not None and 'F' in method_params else default_params['F']

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

    # run the whole algorithm:
    for step in xrange(nr_steps):
        run_step(fit_func, population, dimensionality, population_size, coord_min, coord_max, prog, CR, F)
        bp, bf, bps = get_best_fit(population)
        if bf < best_fitness:
            best_particle, best_fitness, best_pos = bp, bf, bps

        # prog.append(best_fitness)

    if verbose:
        print "Best fitness: {0}".format(best_fitness)

    return prog, best_pos


def run_de(fit_func, dimensionality, population_size, interval, nr_steps, method_params, chart=False, verbose=False):
    if verbose:
        print "SIZE OF POPULATION: ", population_size
        print "FULL MOVES NO: ", nr_steps
        print "FITNESS TO BE CALLED {0} TIMES".format(nr_steps * population_size)

    progress, solution = solve(fit_func, dimensionality, population_size, interval, nr_steps, method_params)
    if chart:
        plt.plot(progress)
        plt.show()

    return solution


if __name__ == '__main__':
    run_de(fit_func=rastrigin_func,
           dimensionality=config.dimensionality,
           population_size=config.population_size,
           interval=(config.coord_min, config.coord_max),
           nr_steps=config.nr_steps,
           method_params={'CR': 0.9, 'F': 0.5},
           chart=True)
