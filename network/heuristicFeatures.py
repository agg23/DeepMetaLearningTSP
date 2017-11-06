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
		randomCost = calculateCost(randomSolution, tsp)

		neighbors = randomNeighborSolutions[i]
		_, neighborCost = bestSolution(tsp, neighbors)

		sum += neighborCost/randomCost

	return sum/len(randomSolutions)

# QNS
def randomNeighborSolutionQuality(tsp, randomSolutions, randomNeighborSolutions):
	sum = 0
	count = 0
	for i in range(len(randomSolutions)):
		randomSolution = randomSolutions[i]
		randomCost = calculateCost(randomSolution, tsp)

		neighbors = randomNeighborSolutions[i]

		for j in range(len(neighbors)):
			neighborCost = calculateCost(neighbors[j], tsp)

			if neighborCost < randomCost:
				sum += 1

		count += len(neighbors)

	return sum/count

# QGS
def greedySolutionQuality(tsp, randomSolutions, greedySolutions):
	sum = 0
	count = 0
	for randomSolution in randomSolutions:
		randomCost = calculateCost(randomSolution, tsp)

		for greedySolution in greedySolutions:
			greedyCost = calculateCost(greedySolution, tsp)

			if greedyCost < randomCost:
				sum += 1

		count += len(greedySolutions)

	return sum/count

# RGR
def averageRatioGreedySolution(tsp, randomSolutions, greedySolutions):
	sum = 0
	count = 0
	for randomSolution in randomSolutions:
		randomCost = calculateCost(randomSolution, tsp)

		for greedySolution in greedySolutions:
			greedyCost = calculateCost(greedySolution, tsp)

			sum += greedyCost/randomCost
			
		count += len(greedySolutions)

	return sum/count