import numpy
import math
import sys

class AntGraph:
	def __init__(self, tsp, beta):
		self.tsp = tsp
		self.avg = self.tsp.averageCost()
		self.num_nodes = tsp.getSize()

		# tau mat contains the amount of phermone at node x,y
		self.tau_mat = numpy.zeros((self.num_nodes, self.num_nodes))

		self.delta_mat = numpy.empty((self.num_nodes, self.num_nodes))
		self.etha_pow_mat = numpy.empty((self.num_nodes, self.num_nodes))

		for i in range(0, self.num_nodes):
			for j in range(0, self.num_nodes):
				adjacent = self.tsp.getAdjacent(i, j)
				cost = self.tsp.getCost(i, j)
				self.delta_mat[i][j] = cost
				if not adjacent or cost == 0:
					# If not adjacent, make it impossible to travel between
					# If cost == 0, shouldn't be accessed anyway, but prevent divide by 0
					cost = sys.maxsize
				self.etha_pow_mat[i][j] = math.pow(1.0 / cost, beta)

	def delta(self, r, s):
		return self.delta_mat[r][s]

	def tau(self, r, s):
		return self.tau_mat[r][s]

	# inner locks most likely not necessary
	def update_tau(self, r, s, val):
		self.tau_mat[r][s] = val

	def reset_tau(self):
		# initial tau 
		self.tau0 = 1.0 / (self.num_nodes * 0.5 * self.avg)

		# print("Average = %f" % (avg,))
		# print("Tau0 = %f" % (self.tau0))

		for r in range(0, self.num_nodes):
			for s in range(0, self.num_nodes):
				self.tau_mat[r][s] = self.tau0
