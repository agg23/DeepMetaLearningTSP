class TSP(object):
	name = None

	def isAsymmetric(self):
		raise NotImplementedError()

	def getCost(self, cityA, cityB):
		raise NotImplementedError()

	def setCost(self, cityA, cityB, cost):
		raise NotImplementedError()

	def getSize(self):
		raise NotImplementedError()