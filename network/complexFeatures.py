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
def networkVulnerability(cache, tsp):
	ge = cache.globalEfficiency
	maxVulnerability = 0
	for city in range(tsp.getSize()):
		vulnerability = networkVulnerabilityAt(city, tsp, ge)

		if vulnerability > maxVulnerability:
			maxVulnerability = vulnerability

	return maxVulnerability

def networkVulnerabilityAt(i, tsp, ge):
	# Since assuming fully connected, first term will always be 1
	return 1/(tsp.getSize() - (tsp.getSize() - 1)) * ge - numpy.mean(1/tsp.costs[i,numpy.nonzero(tsp.costs[i,])])

# CCT
def clusteringCoefficientTransitivity(tsp):
	numberTriangles = 0
	numberTriples = 0

	n = tsp.getSize()

	for i in range(n):
		for j in range(i + 1, n):
			for k in range(j + 1, n):
				numberTriangles += tsp.getAdjacent(i, j) * tsp.getAdjacent(i, k) * tsp.getAdjacent(j, k)
				numberTriples += tsp.getAdjacent(i, j) * tsp.getAdjacent(i, k) + tsp.getAdjacent(j, i) * tsp.getAdjacent(j, k) + tsp.getAdjacent(k, i) * tsp.getAdjacent(k, j)

	return 3 * numberTriangles / numberTriples

# May be different than Kanda's implementation
# ACC
def alternateClusteringCoefficient(tsp):
	sum = 0
	n = tsp.getSize()

	for i in range(n):
		for j in range(n):
			for k in range(j + 1, n):
				numberTriangles = tsp.getAdjacent(i, j) * tsp.getAdjacent(i, k) * tsp.getAdjacent(j, k)
				numberTriples = tsp.getAdjacent(i, j) * tsp.getAdjacent(i, k) + tsp.getAdjacent(j, i) * tsp.getAdjacent(j, k) + tsp.getAdjacent(k, i) * tsp.getAdjacent(k, j)

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
				innerSum += (tsp.getCost(i, j) + tsp.getCost(i, k)) / 2 * tsp.getAdjacent(i, j) * tsp.getAdjacent(i, k) * tsp.getAdjacent(j, k)

		sum += innerSum / (vertexCosts * (connectedEdgeCounts[i] - 1))

	return sum / n

# NCC
def networkCyclicCoefficient(tsp, connectedEdgeCounts):
	sum = 0
	n = tsp.getSize()

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
			adjacent = tsp.getAdjacent(i, j)

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

# CCT, ACC, CCW, NCC, MDV, CED, EDD, TE, PCV, ER, CCA omitted due to irrelevance to fully connected graphs