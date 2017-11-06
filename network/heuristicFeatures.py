from solver.utilities import calculateCost
from .features import bestNeighborSolution

import sys

# QBN
def proportionsNeighborsWithBetterSolution(tsp, randomSolutions, randomNeighborSolutions):
	sum = 0
	for i in range(len(randomSolutions)):
		randomSolution = randomSolutions[i]
		neighbors = randomNeighborSolutions[i]

		randomCost = calculateCost(randomSolution, tsp)

		neighborCost = sys.maxsize

		for i in range(len(neighbors)):
			cost = calculateCost(neighbors[i], tsp)

			if cost < neighborCost:
				neighborCost = cost

		if neighborCost < randomCost:
			sum += 1

	return sum/len(randomSolutions)