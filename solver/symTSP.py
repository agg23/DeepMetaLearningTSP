from solver.tsp import TSP
import numpy

class SymmetricTSP(TSP):
	# Currently identical to asymTSP

	def __init__(self, size):
		# Create a matrix of provided size
		self.costs = numpy.empty(shape=(size, size))

	def isAsymmetric(self):
		return False

	def getCost(self, cityA, cityB):
		return self.costs[cityA][cityB]

	def setCost(self, cityA, cityB, cost):
		self.costs[cityA][cityB] = cost
		self.costs[cityB][cityA] = cost

	def getSize(self):
		return self.costs.shape[0]

	def averageCost(self):
		return numpy.mean(self.costs)