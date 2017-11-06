from solver.utilities import calculateCost
from .features import bestSolution

import sys

# QBN
def proportionsNeighborsWithBetterSolution(tsp, randomSolutions, randomNeighborSolutions):
	sum = 0
	for i in range(len(randomSolutions)):
		randomSolution = randomSolutions[i]
		randomCost = calculateCost(randomSolution, tsp)

		neighbors = randomNeighborSolutions[i]
		_, neighborCost = bestSolution(tsp, neighbors)

		if neighborCost < randomCost:
			sum += 1

	return sum/len(randomSolutions)

# RNS
def averageRatioNeighborsWithBetterSolution(tsp, randomSolutions, randomNeighborSolutions):
	sum = 0.0
	for i in range(len(randomSolutions)):
		randomSolution = randomSolutions[i]
		neighbors = randomNeighborSolutions[i]

		randomCost = calculateCost(randomSolution, tsp)

		_, neighborCost = bestSolution(tsp, neighbors)

		sum += neighborCost/randomCost

	return sum/len(randomSolutions)

# QNS
def randomSolutionQuality(tsp, randomSolutions, randomNeighborSolutions):
	sum = 0
	count = 0
	for i in range(len(randomSolutions)):
		randomSolution = randomSolutions[i]
		neighbors = randomNeighborSolutions[i]

		randomCost = calculateCost(randomSolution, tsp)

		for i in range(len(neighbors)):
			neighborCost = calculateCost(neighbors[i], tsp)

			if neighborCost < randomCost:
				sum += 1

		count += len(neighbors)

	return sum/count