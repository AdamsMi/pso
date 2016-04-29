import random
import copy
from matplotlib import pyplot as plt

from problem import rastrigin_func, Point
from config import GLOBAL_SEED
import config

default_params = {'inertia': 0.75, 'cognitive': 1.5, 'social': 1.5}

counter = 0
progress = []


class Particle(Point):
    def __init__(self, dim, minV, maxV, seed):
        super(Particle, self).__init__(dim, minV, maxV)
        self.randVal = random.Random(seed)
        # self.position = [(maxV - minV) * self.randVal.random() for x in xrange(dim)]
        self.velocity = [(maxV - minV) * self.randVal.random() for x in xrange(dim)]
        # self.currFitness = eval_fitness(self.position)
        self.bestVisitedPosition = copy.copy(self.position)
        self.bestVisitedFitness = None # self.currFitness


def move(fit_func, swarm, dim, bestGlobalPos, minV, maxV, inertia, cognitive, social):
    global counter
    for part in swarm:
        for d in xrange(dim):
            r1 = GLOBAL_SEED.random()
            r2 = GLOBAL_SEED.random()
            myVelocityComponent = inertia * part.velocity[d]

            myBestVisitedPosComponent = cognitive * r2 * (part.bestVisitedPosition[d] - part.position[d])
            globallyBestComponent = social * r1 * (bestGlobalPos[d] - part.position[d])
            part.velocity[d] = myVelocityComponent + myBestVisitedPosComponent + globallyBestComponent
            part.position[d] = min(maxV, max(minV, part.position[d] + part.velocity[d]))

        part.currFitness = fit_func(part.position)
        counter += 1

        if part.currFitness < part.bestVisitedFitness:
            part.bestVisitedFitness = part.currFitness
            part.bestVisitedPosition = copy.copy(part.position)


def solve(fit_func, maxSteps, n, dim, minV, maxV, method_params, sw=None, verbose=False):
    if method_params is None:
        inertia = default_params['inertia']
        cognitive = default_params['cognitive']
        social = default_params['social']
    else:
        inertia = method_params['inertia'] if 'inertia' in method_params else default_params['inertia']
        cognitive = method_params['cognitive'] if 'cognitive' in method_params else default_params['cognitive']
        social = method_params['social'] if 'social' in method_params else default_params['social']

    # creating n random particles
    if n > 0:
        swarm = []
        for i in xrange(n):
            p = Particle(dim, minV, maxV, GLOBAL_SEED.random())
            p.currFitness = fit_func(p.position)
            p.bestVisitedFitness = p.currFitness
            swarm.append(p)
    else:
        swarm = sw

    bestParticle = min(swarm, key=lambda particle: particle.currFitness)
    bestPosition = copy.copy(bestParticle.position)
    bestFitness = bestParticle.currFitness

    for nrOfStep in xrange(maxSteps):
        move(fit_func, swarm, dim, bestPosition, minV, maxV, inertia, cognitive, social)
        bestParticleCandidate = min(swarm, key=lambda particle: particle.currFitness)
        if bestParticleCandidate.currFitness < bestFitness:
            bestPosition = bestParticleCandidate.position
            bestFitness = bestParticleCandidate.currFitness
        if counter % 10 == 0:
            progress.append((counter, bestFitness))
        if nrOfStep % 10 == 0 and verbose:
            print("iteration nr {0}, best fitness: {1} ".format(nrOfStep, bestFitness))
    if verbose:
        print bestPosition
        print "Best fitness: {0}".format(bestFitness)

    return swarm, bestPosition


def run_pso(fit_func, dimensionality, population_size, interval, nr_steps, method_params=None, chart=False, verbose=False):
    # population = []
    if verbose:
        print "SIZE OF POPULATION: ", population_size
        print "FULL SWARM MOVES NO: ", nr_steps
        print "FITNESS TO BE CALLED {0} TIMES".format(nr_steps * population_size)

    coord_min, coord_max = interval
    population, solution = solve(fit_func, nr_steps, population_size, dimensionality, coord_min, coord_max, method_params)
    if chart:
        print progress
        plt.plot([p[0] for p in progress], [p[1] for p in progress])
        plt.show()

    return solution

if __name__ == '__main__':
    run_pso(fit_func=rastrigin_func,
            dimensionality=config.dimensionality,
            population_size=config.population_size,
            interval=(config.coord_min, config.coord_max),
            nr_steps=config.nr_steps,
            method_params={'inertia': 0.75, 'cognitive': 1.5, 'social': 1.5},
            chart=True)
