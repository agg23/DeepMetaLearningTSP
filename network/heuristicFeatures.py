from solver.utilities import calculateCost
from .features import bestSolution, edges

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

def bestSolutionInPair(tsp, pair):
	firstSolutionCost = calculateCost(pair[0], tsp)
	secondSolutionCost = calculateCost(pair[1], tsp)

	if firstSolutionCost < secondSolutionCost:
		return pair[0], firstSolutionCost
	else:
		return pair[1], secondSolutionCost

# QBO
def proportionOffspringBetterSolution(tsp, parentSolutionPairs, childSolutionPairs):
	sum = 0
	for i in range(len(parentSolutionPairs)):
		parentPair = parentSolutionPairs[i]
		childPair = childSolutionPairs[i]

		_, bestParentCost = bestSolutionInPair(tsp, parentPair)
		_, bestChildCost = bestSolutionInPair(tsp, childPair)

		if bestChildCost < bestParentCost:
			sum += 1

	return sum/len(parentSolutionPairs)

# RCP
def averageRatioOffspringBetterSolution(tsp, parentSolutionPairs, childSolutionPairs):
	sum = 0
	for i in range(len(parentSolutionPairs)):
		parentPair = parentSolutionPairs[i]
		childPair = childSolutionPairs[i]

		_, bestParentCost = bestSolutionInPair(tsp, parentPair)
		_, bestChildCost = bestSolutionInPair(tsp, childPair)

		sum += bestChildCost/bestParentCost

	return sum/len(parentSolutionPairs)

# RRQ
def averageTimesOffspringBetterSolution(tsp, parentSolutionPairs, childSolutionPairs):
	sum = 0
	for i in range(len(parentSolutionPairs)):
		parentPair = parentSolutionPairs[i]
		childPair = childSolutionPairs[i]

		for j in range(2):
			childCost = calculateCost(childPair[j], tsp)

			for k in range(2):
				parentCost = calculateCost(parentPair[k], tsp)

				if childCost < parentCost:
					sum += 1

	return sum/(len(parentSolutionPairs) * 4)

# ISE
def averageSharedEdges(tsp, greedyEdges):
	sum = 0
	n = len(greedyEdges)

	for i in range(n):
		firstEdgeSet = greedyEdges[i]

		for j in range(n):
			secondEdgeSet = greedyEdges[i]

			sum += len(firstEdgeSet.intersection(secondEdgeSet)) / n

	return 2 * sum / (n * (n - 1))

# RFM
def relativeFrequencyCommonGreedyEdge(tsp, greedyEdges):
	edgeMap = {}

	# Build frequency map of edges
	for edgeSet in greedyEdges:
		for edge in edgeSet:
			if edge in edgeMap:
				edgeMap[edge] += 1
			else:
				edgeMap[edge] = 1

	# Get highest frequency edge
	count = 0
	maxEdge = None
	for edge in edgeMap:
		edgeCount = edgeMap[edge]

		if edgeCount > count:
			count = edgeCount
			maxEdge = edge

	sum = 0

	for edgeSet in greedyEdges:
		if maxEdge in edgeSet:
			sum += 1

	return sum / len(greedyEdges)
