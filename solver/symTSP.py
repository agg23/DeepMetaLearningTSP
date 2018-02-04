from solver.tsp import TSP
import numpy
import sys

class SymmetricTSP(TSP):
	# Currently identical to asymTSP

	def __init__(self, size):
		# Create a matrix of provided size
		self.costs = numpy.empty(shape=(size, size))
		super().__init__(size)

	def isAsymmetric(self):
		return False

	def getCost(self, cityA, cityB):
		if not self.getAdjacent(cityA, cityB):
			return sys.maxsize
		
		return self.costs[cityA][cityB]

	def setCost(self, cityA, cityB, cost):
		self.costs[cityA][cityB] = cost
		self.costs[cityB][cityA] = cost

		# If cost set, then must be adjacent
		self.setAdjacent(cityA, cityB, True)
		self.setAdjacent(cityB, cityA, True)

	def getSize(self):
		return self.costs.shape[0]

	def averageCost(self):
		return numpy.mean(self.costs)