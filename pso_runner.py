import random
import copy
import math

INERTIA = 0.75
COGNITIVE = 1.5
SOCIAL = 1.5

GLOBAL_SEED = random.Random(0)
NR_ISLANDS = 5
NR_ISOLATED_STEPS = 100
NR_COMMON_STEPS = 100
DIM_OF_PARTICLES = 3
NR_PARTICLES_PER_ISLAND = 50
MIN_V = -50
MAX_V = 50


def rastriginFunc(currPos):
	fitness = 10*len(currPos)
	for el in currPos:
		fitness += el**2 - (10*math.cos(2*math.pi*el))
	return fitness


def evalFitness(pos):
    return rastriginFunc(pos)

class Particle:
    def __init__(self, dim, minV, maxV, seed):
        self.randVal = random.Random(seed)
        self.position = [(maxV - minV)*self.randVal.random() for x in xrange(dim)]
        self.velocity = [(maxV - minV)*self.randVal.random() for x in xrange(dim)]
        self.currFitness = evalFitness(self.position)
        self.bestVisitedPosition = copy.copy(self.position)
        self.bestVisitedFitness = self.currFitness

    def __str__(self):
        return str(self.position) + "\nfitness: " + str(self.currFitness)



def move(swarm, dim, bestGlobalPos, minV, maxV):

    for part in swarm:
        for d in xrange(dim):
            r1 = GLOBAL_SEED.random()
            r2 = GLOBAL_SEED.random()
            myVelocityComponent = INERTIA * part.velocity[d]

            myBestVisitedPosComponent = COGNITIVE * r2 * (part.bestVisitedPosition[d] - part.position[d])
            globallyBestComponent = SOCIAL * r1 * (bestGlobalPos[d] - part.position[d])
            part.velocity[d] = myVelocityComponent + myBestVisitedPosComponent + globallyBestComponent
            part.position[d] = min(maxV, max(minV, part.position[d] + part.velocity[d]))
        part.currFitness = evalFitness(part.position)

        if part.currFitness < part.bestVisitedFitness:
            part.bestVisitedFitness = part.currFitness
            part.bestVisitedPosition = copy.copy(part.position)

def solve(maxSteps, n, dim, minV, maxV, sw = None, verbose = False):

    #creating n random particles
    if n>0:
        swarm = [Particle(dim, minV, maxV, GLOBAL_SEED.random()) for i in range(n)]
    else:
        swarm = sw
    bestParticle = min(swarm, key = lambda particle: particle.currFitness)
    bestPosition = copy.copy(bestParticle.position)
    bestFitness = evalFitness(bestPosition)
    for nrOfStep in xrange(maxSteps):
        move(swarm, dim, bestPosition, minV, maxV)
        bestParticleCandidate = min(swarm, key = lambda particle: particle.currFitness)
        if bestParticleCandidate.currFitness < bestFitness:
            bestPosition = bestParticleCandidate.position
            bestFitness = bestParticleCandidate.currFitness

        if nrOfStep % 10 ==0:
            print("iteration nr {0}, best fitness: {1} ".format(nrOfStep, bestFitness))
    if verbose:
        print bestPosition

    return swarm

if __name__ == '__main__':
    population = []
    for x in xrange(NR_ISLANDS):
        print "-------------------------nr of island {0}-------------------------------".format(x)
        population += solve(NR_ISOLATED_STEPS, NR_PARTICLES_PER_ISLAND, DIM_OF_PARTICLES, MIN_V, MAX_V)
    print "SIZE OF POPULATION: ", len(population)
    solve(NR_ISOLATED_STEPS, 0, DIM_OF_PARTICLES, MIN_V, MAX_V, sw=population, verbose=True)