class SymmetricTSP(TSP):
	# Currently identical to asymTSP

	def __init__(self, size):
		# Create a matrix of provided size
		self.costs = numpy.empty(shape=(size, size))

	def isAsymmetric():
		return False

	def getCost(cityA, cityB):
		return self.costs[cityA][cityB]

	def setCost(cityA, cityB, cost):
		self.costs[cityA][cityB] = cost
		self.costs[cityB][cityA] = cost

	def getSize():
		return self.costs.shape[0]