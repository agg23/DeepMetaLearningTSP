import sys
import numpy

from .features import vertexCost, buildVertexCosts

def numberVerticies(tsp):
	return tsp.getSize()

def lowestVertexCost(costs):
	return numpy.amin(costs)

def highestVertexCost(costs):
	return numpy.amax(costs)

def averageVertexCost(costs):
	return numpy.mean(costs)

def standardDeviationVertexCost(costs):
	return numpy.std(costs)

def medianVertexCost(costs):
	return numpy.median(costs)

def sumCostNearestNeighbor(tsp):
	sumValue = 0
	for city in range(0, tsp.getSize()):
		minCost = sys.maxsize

		for innerCity in range(0, tsp.getSize()):
			if city == innerCity:
				continue

			cost = tsp.getCost(city, innerCity)
			if cost < minCost:
				minCost = cost

		sumValue += minCost

	return sumValue

def numberEdges(tsp):
	return numpy.sum(tsp.adjacent)

def lowestEdgeCost(tsp):
	return numpy.amin(tsp.costs)

def highestEdgeCost(tsp):
	return numpy.amax(tsp.costs)

def averageEdgeCost(tsp):
	return numpy.mean(tsp.costs)

def standardDeviationEdgeCost(tsp):
	return numpy.std(tsp.costs)

def medianEdgeCost(tsp):
	return numpy.median(tsp.costs)

def sumNLowestEdgeCost(tsp, n):
	sortedCosts = numpy.sort(tsp.costs, axis=None)

	sumValue = 0
	for i in range(0, max(n, tsp.getSize())):
		sumValue += sortedCosts[i]

	return sumValue