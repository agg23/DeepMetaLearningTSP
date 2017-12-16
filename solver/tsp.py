import numpy

class TSP(object):
	def __init__(self, size):
		self.adjacent = numpy.zeros(shape=(size, size), dtype=bool)
		self.name = None

	def getName(self):
		return self.name

	def setName(self, newName):
		self.name = newName

	def isAsymmetric(self):
		raise NotImplementedError()

	def getCost(self, cityA, cityB):
		raise NotImplementedError()

	def setCost(self, cityA, cityB, cost):
		raise NotImplementedError()

	def getAdjacent(self, cityA, cityB):
		return self.adjacent[cityA][cityB]

	def setAdjacent(self, cityA, cityB, adjacent):
		self.adjacent[cityA][cityB] = adjacent

	def getSize(self):
		raise NotImplementedError()

	def averageCost(self):
		raise NotImplementedError()