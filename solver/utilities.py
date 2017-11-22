import numpy
import random

def generateInitialSolution(tsp):
	return numpy.random.permutation(tsp.getSize())

def calculateCost(solution, tsp):
	cost = 0

	shape = solution.shape

	if len(shape) == 0 or shape[0] < 2:
		return cost

	previous = None
	current = solution[0]

	for i in range(1, solution.shape[0]):
		temp = solution[i]

		cost += tsp.getCost(current, temp)
 
		previous = current
		current = temp

	# Add cost of returning from last to first
	cost += tsp.getCost(current, solution[0])

	return cost