import numpy

class AntGraph:
	def __init__(self, tsp):
		self.tsp = tsp
		self.num_nodes = tsp.getSize()

		# tau mat contains the amount of phermone at node x,y
		self.tau_mat = numpy.zeros((self.num_nodes, self.num_nodes))

	def delta(self, r, s):
		return self.tsp.getCost(r, s)

	def tau(self, r, s):
		return self.tau_mat[r][s]

	# 1 / delta = eta or etha 
	def etha(self, r, s):
		return 1.0 / self.delta(r, s)

	# inner locks most likely not necessary
	def update_tau(self, r, s, val):
		self.tau_mat[r][s] = val

	def reset_tau(self):
		avg = self.tsp.averageCost()

		# initial tau 
		self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)

		# print("Average = %f" % (avg,))
		# print("Tau0 = %f" % (self.tau0))

		for r in range(0, self.num_nodes):
			for s in range(0, self.num_nodes):
				self.tau_mat[r][s] = self.tau0
