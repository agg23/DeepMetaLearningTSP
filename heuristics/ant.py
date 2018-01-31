import math
import random
import sys
import numpy

class Ant:
	def __init__(self, ID, start_node, colony, q0, rho):
		self.ID = ID
		self.start_node = start_node
		self.colony = colony

		self.curr_node = self.start_node
		self.graph = self.colony.graph
		self.path_vec = []
		self.path_vec.append(self.start_node)
		self.path_cost = 0

		# same meaning as in standard equations
		#self.Q0 = 1  # Q0 = 1 works just fine for 10 city case (no explore)
		self.q0 = q0
		self.rho = rho

		# store the nodes remaining to be explored here
		self.nodes_to_visit = {}

		for i in range(0, self.graph.num_nodes):
			if i != self.start_node:
				self.nodes_to_visit[i] = i

		# create n X n matrix 0'd out to start
		self.path_mat = numpy.zeros((self.graph.num_nodes, self.graph.num_nodes))

	# overide Thread's run()
	def run(self):
		graph = self.colony.graph
		while not self.end():
			# we need exclusive access to the graph
			new_node = self.state_transition_rule(self.curr_node)
			self.path_cost += graph.delta(self.curr_node, new_node)

			self.path_vec.append(new_node)
			self.path_mat[self.curr_node][new_node] = 1  #adjacency matrix representing path

			# print("Ant %s : %s, %s" % (self.ID, self.path_vec, self.path_cost,))
			
			self.local_updating_rule(self.curr_node, new_node)

			self.curr_node = new_node

		# don't forget to close the tour
		self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])

		# send our results to the colony
		self.colony.update(self)
		# print("Ant thread %d terminating.\n" % (self.ID))

		# allows thread to be restarted (calls Thread.__init__)
		# self.__init__(self.ID, self.start_node, self.colony)

	def end(self):
		return not self.nodes_to_visit 

	# described in report -- determines next node to visit after curr_node
	def state_transition_rule(self, curr_node):
		graph = self.colony.graph
		q = random.random()
		max_node = -1

		etha_pow_mat = graph.etha_pow_mat[curr_node]
		tau_mat = graph.tau_mat[curr_node]

		nodes = list(self.nodes_to_visit.values())

		mult_mat = numpy.multiply(tau_mat[nodes], etha_pow_mat[nodes])

		if q < self.q0:
			# print("Exploitation")
			max_node = nodes[numpy.argmax(mult_mat)]

		else:
			# print("Exploration")
			sum = 0
			node = -1

			sum = numpy.sum(mult_mat)
			# if sum == 0:
			# 	raise Exception("sum = 0")

			avg = sum / len(nodes)

			# print("avg = %f\n" % (avg))

			for i, node in enumerate(nodes):
				p = mult_mat[i]
				if p > avg:
					# print("p = %s" % (p,))
					max_node = node

			if max_node == -1:
				max_node = node
		
		if max_node < 0:
			raise Exception("max_node < 0")

		del self.nodes_to_visit[max_node]
		
		return max_node

	# phermone update rule for indiv ants
	def local_updating_rule(self, curr_node, next_node):
		graph = self.colony.graph
		val = (1 - self.rho) * graph.tau(curr_node, next_node) + (self.rho * graph.tau0)
		graph.update_tau(curr_node, next_node, val)

