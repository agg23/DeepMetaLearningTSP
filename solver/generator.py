import random

from .asymTSP import AsymmetricTSP
from .symTSP import SymmetricTSP
from .loader import euclidianDistance3D

class Generator(object):
	def generateSymmetric(self, n):
		# Generates points in 3D space, bounded between 0 and 100
		points = []
		for i in range(n):
			x = random.uniform(0, 100)
			y = random.uniform(0, 100)
			z = random.uniform(0, 100)

			points.append((x, y, z))

		tsp = SymmetricTSP(n)

		for i in range(n):
			p1 = points[i]

			for j in range(n):
				if i < j:
					p2 = points[j]
					cost = euclidianDistance3D(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])
					tsp.setCost(i, j, cost)
					tsp.setCost(j, i, cost)

			# Add diagonal
			tsp.setCost(i, i, 0)
			tsp.setAdjacent(i, i, False)

		return tsp

	def generateAsymmetric(self, n):
		tsp = AsymmetricTSP(n)

		# Generate costs bounded between 0 and 1000 for each
		for i in range(n):
			for j in range(n):
				cost = random.uniform(0, 1000)

				tsp.setCost(i, j, cost)

			# Add diagonal
			tsp.setCost(i, i, 0)
			tsp.setAdjacent(i, i, False)

		return tsp
