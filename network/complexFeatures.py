import sys
import numpy
import math

from .features import dijkstra, dijkstraConnectedPath, dijkstraShortestPathWithData
from .simpleFeatures import numberEdges

# May be different than Kanda's implementation
# AGD
def averageShortestPathGeodesicDistance(tsp):
	costSum = 0
	edgeCount = 0
	for city in range(tsp.getSize()):
		visited, paths = dijkstra(tsp, city)

		for innerCity in range(tsp.getSize()):
			if city == innerCity:
				continue

			_destination = paths[innerCity]

			while _destination != city:
				_destination = paths[_destination]

			shortestPathCost = visited[innerCity]
			costSum += shortestPathCost
			edgeCount += 1

	return costSum/edgeCount

# AGD v2
def averageGeodesicDistance(tsp):
	return numpy.mean(tsp.costs[numpy.nonzero(tsp.costs)])

# GE
def globalEfficiency(tsp):
	return numpy.mean(1/tsp.costs[numpy.nonzero(tsp.costs)])

# HM
def harmonicMeanGeodesicDistance(tsp):
	# Number of edges minus diagonal
	return (tsp.getSize() * (tsp.getSize() - 1)) * numpy.sum(1/tsp.costs[numpy.nonzero(tsp.costs)])

# NV
def networkVulnerability(tsp, globalEfficiency):
	maxVulnerability = 0
	for city in range(tsp.getSize()):
		vulnerability = networkVulnerabilityAt(city, tsp, globalEfficiency)

		if vulnerability > maxVulnerability:
			maxVulnerability = vulnerability

	return maxVulnerability

def networkVulnerabilityAt(i, tsp, globalEfficiency):
	# Since assuming fully connected, first term will always be 1
	return 1/(tsp.getSize() - (tsp.getSize() - 1)) * globalEfficiency - numpy.mean(1/tsp.costs[i,numpy.nonzero(tsp.costs[i,])])

# CCT
def clusteringCoefficientTransitivity(tsp):
	numberTriangles = 0
	numberTriples = 0

	n = tsp.getSize()

	for i in range(n):
		for j in range(i + 1, n):
			ij = tsp.adjacent[i, j]
			ji = tsp.adjacent[i, j]
			for k in range(j + 1, n):
				numberTriangles += int(ij and tsp.adjacent[i, k] and tsp.adjacent[j, k])
				numberTriples += int(ij and tsp.adjacent[i, k]) + int(ji and tsp.adjacent[j, k]) + int(tsp.adjacent[k, i] and tsp.adjacent[k, j])

	return 3 * numberTriangles / numberTriples

# May be different than Kanda's implementation
# ACC
def alternateClusteringCoefficient(tsp):
	sum = 0
	n = tsp.getSize()

	for i in range(n):
		for j in range(n):
			ij = tsp.adjacent[i, j]
			ji = tsp.adjacent[i, j]
			for k in range(j + 1, n):
				numberTriangles = int(ij and tsp.adjacent[i, k] and tsp.adjacent[j, k])
				numberTriples = int(ij and tsp.adjacent[i, k]) + int(ji and tsp.adjacent[j, k]) + int(tsp.adjacent[k, i] and tsp.adjacent[k, j])

				sum += numberTriangles / numberTriples

	return sum / n

# CCW
def weightedClusteringCoefficient(tsp, connectedEdgeCounts):
	sum = 0
	n = tsp.getSize()

	for i in range(n):
		vertexCosts = 0
		for j in range(n):
			if i == j:
				continue

			vertexCosts += tsp.getCost(i, j)

		innerSum = 0
		for j in range(n):
			for k in range(j + 1, n):
				innerSum += (int(tsp.costs[i, j]) + int(tsp.costs[i, k])) / 2 * int(tsp.adjacent[i, j] and tsp.adjacent[i, k] and tsp.adjacent[j, k])

		sum += innerSum / (vertexCosts * (connectedEdgeCounts[i] - 1))

	return sum / n

# NCC
def networkCyclicCoefficient(tsp, connectedEdgeCounts):
	sum = 0
	n = tsp.getSize()

	if not tsp.isAsymmetric():
		# Cycles are all length 3. Short circuit
		innerSum = n * n / 3
		for i in range(n):
			sum += 2 * innerSum / (connectedEdgeCounts[i] * (connectedEdgeCounts[i] - 1))
	else:
		for i in range(n):
			innerSum = 0
			for j in range(n):
				if j == i:
					continue

				visited = None
				paths = None
				for k in range(n):
					if k == i or k == j:
						continue
					# Optimization: Only run dijkstra's if both verticies are connected to i
					if tsp.getAdjacent(i, j) and tsp.getAdjacent(i, k):
						length = 0
						if tsp.getAdjacent(j, k):
							# Optimization: Short circuit if shortest path is a simple triangle
							length = 2
						else:
							# Optimiaztion: Lazy load dijkstra's for each j
							if visited == None:
								visited, paths = dijkstraConnectedPath(tsp, j)

							length, _ = dijkstraShortestPathWithData(visited, paths, j, k)

						# Add 1 to path length (as we need to include the edge from either i to j or i to k)
						innerSum += 1 / (length + 1)

			sum += 2 * innerSum / (connectedEdgeCounts[i] * (connectedEdgeCounts[i] - 1))

	return sum / n

# MDV
def maxVertexDegree(connectedEdgeCounts):
	return max(connectedEdgeCounts)

# CED
def edgeDegreeCorrelation(tsp, connectedEdgeCounts):
	firstNumerator = 0
	secondNumerator = 0
	firstDenominator = 0
	n = tsp.getSize()
	m = numberEdges(tsp)

	for i in range(n):
		for j in range(i + 1, n):
			# Optimization: Process all loops at once
			mi = connectedEdgeCounts[i]
			mj = connectedEdgeCounts[j]
			adjacent = int(tsp.getAdjacent(i, j))

			firstNumerator += mi * mj * adjacent
			secondNumerator += (mi + mj) * adjacent
			firstDenominator += (mi * mi + mj * mj) * adjacent

	secondDenominator = pow(secondNumerator / (2 * m), 2)
	return (firstNumerator / m - secondDenominator) / (firstDenominator / (2 * m) - secondDenominator)

# EDD
def entropyDegreeDistribution(tsp):
	# TODO: Finish
	pass

# TE
def targetEntropy(tsp):
	sum = 0
	n = tsp.getSize()

	for i in range(n):
		for j in range(n):
			if tsp.getAdjacent(j, i):
				cost = tsp.getCost(i, j)
				if cost != 0:
					sum += cost * math.log(cost, 2)

	return - sum / n

# PCV
def vertexParticipationCoefficient(tsp):
	# TODO: Finish
	pass

# ER
def edgeReciprocity(tsp):
	sum = 0
	n = tsp.getSize()

	for i in range(n):
		for j in range(n):
			if tsp.getAdjacent(i, j) and tsp.getAdjacent(j, i):
				sum += 1

	return sum / numberEdges(tsp)

# CCA
def adjacencyCorrelationCoefficient(tsp):
	numeratorSum = 0
	denominatorSum = 0
	n = tsp.getSize()

	aBar = numpy.mean(tsp.adjacent)

	for i in range(n):
		for j in range(n):
			numeratorSum += (int(tsp.getAdjacent(i, j)) - aBar) * (int(tsp.getAdjacent(j, i)) - aBar)
			denominatorSum += pow((int(tsp.getAdjacent(i, j)) - aBar), 2)

	# Instead of returning infinity for dividing by 0, return -1
	if denominatorSum == 0:
		return -1

	return numeratorSum / denominatorSum
