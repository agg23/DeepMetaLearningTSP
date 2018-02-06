import numpy
import random

def generateInitialSolution(tsp):
	count = 0
	permutation = numpy.random.permutation(tsp.getSize())

	while(not validateSolution(permutation, tsp)):
		permutation = numpy.random.permutation(tsp.getSize())

		count += 1

	return permutation

def validateSolution(solution, tsp):
	current = solution[0]

	for i in range(1, solution.shape[0]):
		temp = solution[i]

		if not tsp.getAdjacent(current, temp):
			# No edge from current to temp
			return False

		current = temp

	if not tsp.getAdjacent(current, solution[0]):
		# No last node to first
		return False

	return True

def calculateCost(solution, tsp):
	cost = 0

	shape = solution.shape

	if len(shape) == 0 or shape[0] < 2:
		return cost

	current = solution[0]

	for i in range(1, solution.shape[0]):
		temp = solution[i]

		cost += tsp.getCost(current, temp)
 
		current = temp

	# Add cost of returning from last to first
	cost += tsp.getCost(current, solution[0])

	return cost