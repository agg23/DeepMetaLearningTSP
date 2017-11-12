import sys
import numpy

from .features import dijkstra

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

# CCT, ACC, CCW, NCC, MDV, CED, EDD, TE, PCV, ER, CCA omitted due to irrelevance to fully connected graphs