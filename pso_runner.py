import random
import copy
import math
from matplotlib import pyplot as plt
INERTIA = 0.75
COGNITIVE = 1.5
SOCIAL = 1.5

GLOBAL_SEED = random.Random(0)
NR_SWARM_STEPS = 100
DIM_OF_PARTICLES = 3
PARTICLES_NO = 25
MIN_V = -50
MAX_V = 50

counter = 0
progress = []

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
    global counter
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
        counter +=1
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
        if counter % 100 == 0:
            progress.append((counter, bestFitness))
        if nrOfStep % 10 ==0 and verbose:
            print("iteration nr {0}, best fitness: {1} ".format(nrOfStep, bestFitness))
    if verbose:
        print bestPosition

    return swarm

if __name__ == '__main__':
    population = []
    print "SIZE OF POPULATION: ", PARTICLES_NO
    print "FULL SWARM MOVES NO: ", NR_SWARM_STEPS
    print "FITNESS TO BE CALLED {0} TIMES".format(NR_SWARM_STEPS * PARTICLES_NO)

    population += solve(NR_SWARM_STEPS, PARTICLES_NO, DIM_OF_PARTICLES, MIN_V, MAX_V)
    print progress
    plt.plot([p[1] for p in progress],[p[0] for p in progress])
    plt.show()