import random
import copy

INERTIA = 0.75
COGNITIVE = 1.5
SOCIAL = 1.5

GLOBAL_SEED = random.Random(0)

def evalFitness(pos):
    return sum(pos)

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



def move(swarm, dim, bestGlobal, minV, maxV):

    for part in swarm:
        for d in xrange(dim):
            r1 = GLOBAL_SEED.random()
            r2 = GLOBAL_SEED.random()
            myVelocityComponent = INERTIA * part.velocity[d]
            myBestVisitedPosComponent = COGNITIVE * r2 * (part.bestVisitedPosition[d] - part.position[d])
            globallyBestComponent = SOCIAL * r1 * (bestGlobal.bestVisitedPosition[d] - part.position[d])
            part.velocity[d] = myVelocityComponent + myBestVisitedPosComponent + globallyBestComponent
            part.position[d] = min(maxV, max(minV, part.position[d] + part.velocity[d]))
        part.currFitness = evalFitness(part.position)

        if part.currFitness < part.bestVisitedFitness:
            part.bestVisitedFitness = part.currFitness
            part.bestVisitedPosition = copy.copy(part.position)

def solve(maxSteps, n, dim, minV, maxV):

    #creating n random particles
    swarm = [Particle(dim, minV, maxV, GLOBAL_SEED.random()) for n in range(dim)]
    bestParticle = min(swarm, key = lambda particle: particle.currFitness)
    for nrOfStep in xrange(maxSteps):
        move(swarm, dim, bestParticle, minV, maxV)
        bestParticle = min(swarm, key = lambda particle: particle.currFitness)
        print("iteration nr {0}, best particle: ".format(nrOfStep))
        print(bestParticle)


if __name__ == '__main__':
    solve(10, 5, 3, 0.0, 4.0)