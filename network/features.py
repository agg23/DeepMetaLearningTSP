# Utilities

from collections import defaultdict, deque
from solver.utilities import calculateCost
from heuristics.genetic import crossover
import sys
import numpy

def vertexCost(tsp, index):
	sumValue = 0

	for i in range(tsp.getSize()):
		sumValue += tsp.getCost(i, index)
		sumValue += tsp.getCost(index, i)

	# 2 times as many costs as points
	return sumValue/(tsp.getSize()*2)

def buildVertexCosts(tsp):
	costs = numpy.empty(tsp.getSize())

	for city in range(tsp.getSize()):
		costs[city] = vertexCost(tsp, city)

	return costs

# From Gist https://gist.github.com/mdsrosa/c71339cb23bc51e711d8
def dijkstra(tsp, initial):
	visited = {initial: 0}
	path = {}

	nodes = set(range(tsp.getSize()))

	while nodes:
		min_node = None
		for node in nodes:
			if node in visited:
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node
		if min_node is None:
			break

		nodes.remove(min_node)
		current_weight = visited[min_node]

		for second_node in range(tsp.getSize()):
			try:
				weight = current_weight + tsp.getCost(min_node, second_node)
			except:
				continue
			if second_node not in visited or weight < visited[second_node]:
				visited[second_node] = weight
				path[second_node] = min_node

	return visited, path

def dijkstraShortestPath(tsp, origin, destination):
	visited, paths = dijkstra(tsp, origin)
	return dijkstraShortestPathWithData(visited, paths, origin, destination)

# Builds a map of the shortest connected paths (used for asymmetrical TSP instances)
def dijkstraConnectedPath(tsp, initial):
	visited = {initial: 0}
	path = {}

	nodes = set(range(tsp.getSize()))

	while nodes:
		min_node = None
		for node in nodes:
			if node in visited:
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node
		if min_node is None:
			break

		nodes.remove(min_node)
		current_weight = visited[min_node]

		for second_node in range(tsp.getSize()):
			try:
				connected = tsp.getAdjacent(min_node, second_node)
				# A large value (big M)
				weight = 100000
				if connected:
					weight = 1
				weight = current_weight + weight
			except:
				continue
			if second_node not in visited or weight < visited[second_node]:
				visited[second_node] = weight
				path[second_node] = min_node

	return visited, path

def dijkstraShortestConnectedPath(tsp, origin, destination):
	visited, paths = dijkstraConnectedPath(tsp, origin)
	return dijkstraShortestPathWithData(visited, paths, origin, destination)

def dijkstraShortestPathWithData(visited, paths, origin, destination):
	full_path = deque()
	_destination = paths[destination]

	while _destination != origin:
		full_path.appendleft(_destination)
		_destination = paths[_destination]

	full_path.appendleft(origin)
	full_path.append(destination)

	return visited[destination], list(full_path)

# Solution selection

def randomSolutions(tsp, n):
	solutions = []

	for i in range(n):
		solutions.append(numpy.random.permutation(tsp.getSize()))

	return solutions

def solutionPairs(tsp, randomSolutions, n):
	numberRandomSolutions = len(randomSolutions)

	solutions = []

	i = 0
	while i < n:
		first = numpy.random.randint(numberRandomSolutions)
		second = numpy.random.randint(numberRandomSolutions)

		if first == second:
			continue

		solutions.append((randomSolutions[first], randomSolutions[second]))

		i += 1

	return solutions

def childrenSolutionPairs(tsp, parentSolutionPairs):
	solutions = []

	for parentPair in parentSolutionPairs:
		firstChild, secondChild = crossover(tsp, parentPair[0], parentPair[1])

		solutions.append((firstChild, secondChild))

	return solutions

def edges(tsp, solutions):
	allSolutionEdges = []

	for solution in solutions:
		solutionEdges = set()

		for i in range(1, len(solution)):
			first = solution[i - 1]
			second = solution[i]

			solutionEdges.add((first, second))

		if len(solution) > 1:
			# Add final solution
			solutionEdges.add((solution[len(solution) - 1], solution[0]))

		allSolutionEdges.append(solutionEdges)

	return allSolutionEdges

def connectedEdgeCount(tsp, i):
	sum = 0

	for j in range(tsp.getSize()):
		if i == j:
			continue

		sum += tsp.getAdjacent(i, j)

	return sum

def connectedEdgeCounts(tsp):
	edgeCounts = []

	for i in range(tsp.getSize()):
		edgeCounts.append(connectedEdgeCount(tsp, i))

	return edgeCounts

def greedySolutions(tsp, n):
	solutions = []

	for i in range(n):
		initial = numpy.random.randint(tsp.getSize())
		solution = [initial]

		while len(solution) < tsp.getSize():
			last = solution[-1]

			minCity = 0
			minCost = sys.maxsize
			for city in range(tsp.getSize()):
				if city == last or city in solution:
					continue

				cost = tsp.getCost(last, city)

				if cost < minCost:
					minCity = city
					minCost = cost

			solution.append(minCity)

		solutions.append(numpy.array(solution))

	return solutions

def neighborSolutions(tsp, solution, n):
	solutions = []

	for i in range(n):
		newSolution = numpy.copy(solution)
		selected = numpy.random.randint(tsp.getSize())

		if selected == tsp.getSize() - 1:
			# Swap with first element
			newSolution[selected] = solution[0]
			newSolution[0] = solution[selected]
		else:
			newSolution[selected] = solution[selected + 1]
			newSolution[selected + 1] = solution[selected]

		solutions.append(newSolution)

	return solutions

def bestSolution(tsp, solutions):
	bestSolution = None
	minCost = sys.maxsize

	for i in range(len(solutions)):
		cost = calculateCost(solutions[i], tsp)

		if cost < minCost:
			minCost = cost
			bestSolution = solutions[i]

	return bestSolution, minCost

def bestNeighborSolution(tsp, solution, n):
	solutions = neighborSolutions(tsp, solution, n)

	return bestSolution(tsp, solutions)
