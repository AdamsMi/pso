import numpy.random as npr
import matplotlib.pyplot as plt

from problem import eval_fitness, Point
from config import COORD_MIN, COORD_MAX, DIMENSIONALITY, NR_STEPS, POPULATION_SIZE


# helper function for random indices:
def randint(high=POPULATION_SIZE):
    return npr.randint(0, high)


# pick three indices different from each other and from x:
def pick_3_diff(population, i):
    a_i = randint()
    while a_i == i:
        a_i = randint()

    b_i = randint()
    while b_i == i or b_i == a_i:
        b_i = randint()

    c_i = randint()
    while c_i == i or c_i == a_i or c_i == b_i:
        c_i = randint()

    a = population[a_i]
    b = population[b_i]
    c = population[c_i]

    return a, b, c


# run a single step of the algorithm:
def run_step(population, CR, F):
    # for every agent in the population:
    for idx in xrange(POPULATION_SIZE):
        x = population[idx]
        # pick 3 different agents randomly:
        a, b, c = pick_3_diff(population, x)

        R = randint(DIMENSIONALITY)

        # new, candidate position:
        y = Point(DIMENSIONALITY, COORD_MIN, COORD_MAX)
        for i in xrange(DIMENSIONALITY):
            r_i = npr.random()
            if r_i < CR or i == R:
                y.position[i] = a.position[i] + F * (b.position[i] - c.position[i])
            else:
                y.position[i] = x.position[i]

        y.currFitness = eval_fitness(y.position)
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
def run_de(CR=0.9, F=0.5):
    # initialize the population:
    population = []
    for i in xrange(POPULATION_SIZE):
        population.append(Point(DIMENSIONALITY, COORD_MIN, COORD_MAX))

    prog = []
    best_particle, best_fitness, best_pos = get_best_fit(population)
    prog.append(best_fitness)

    # run the whole algorithm:
    for step in xrange(NR_STEPS):
        run_step(population, CR, F)
        bp, bf, bps = get_best_fit(population)
        if bf < best_fitness:
            best_particle, best_fitness, best_pos = bp, bf, bps

        prog.append(best_fitness)

    return prog

if __name__ == '__main__':
    print "SIZE OF POPULATION: ", POPULATION_SIZE
    print "FULL MOVES NO: ", NR_STEPS
    print "FITNESS TO BE CALLED {0} TIMES".format(NR_STEPS * POPULATION_SIZE)
    progress = run_de()
    plt.plot(progress)
    plt.show()
