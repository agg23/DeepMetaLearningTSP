# Utilities

def vertexCost(tsp, index):
	sumValue = 0

	for i in range(0, tsp.getSize()):
		sumValue += tsp.getCost(i, index)
		sumValue += tsp.getCost(index, i)

	# 2 times as many costs as points
	return sumValue/(tsp.getSize()*2)

def buildVertexCosts(tsp):
	costs = numpy.array(tsp.getSize())

	for city in range(0, tsp.getSize()):
		costs[city] = vertexCost(tsp, city)

	return costs
