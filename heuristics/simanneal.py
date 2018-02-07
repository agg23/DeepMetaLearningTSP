from solver.utilities import generateInitialSolution, calculateCost
import random
import time
from simanneal import Annealer

class SimulatedAnnealing(Annealer):
	def __init__(self, tsp):
		self.tsp = tsp
		super(SimulatedAnnealing, self).__init__(generateInitialSolution(tsp))

	def anneal(self):
		self.startTime = time.time()
		return super(SimulatedAnnealing, self).anneal()

	def move(self):
		"""Swaps two cities in the route."""
		a = random.randint(0, len(self.state) - 1)
		b = random.randint(0, len(self.state) - 1)
		self.state[a], self.state[b] = self.state[b], self.state[a]

		if time.time() - self.startTime > self.timelimit:
			self.user_exit = True

	def energy(self):
		"""Calculates the length of the route."""
		return calculateCost(self.state, self.tsp)