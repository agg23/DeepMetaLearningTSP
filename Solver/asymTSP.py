class AsymmetricTSP(TSP):
	def __init__(self, size):
		# Create a matrix of provided size
		self.costs = numpy.empty(shape=(size, size))

	def isAsymmetric():
		return True

	def getCost(cityA, cityB):
		return self.costs[cityA][cityB]

	def setCost(cityA, cityB, cost):
		self.costs[cityA][cityB] = cost

	def getSize():
		return self.costs.shape[0]