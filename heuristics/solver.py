import sys
from .antcolony import AntColony
from .antgraph import AntGraph

import heuristics.tabu as tabu
import heuristics.grasp as grasp
from .simanneal import SimulatedAnnealing
from .genetic import Genetic

def solveTabu(tsp, maxCandidates, maxTabu, maxIterations, timeLimit):
	return tabu.search(tsp, maxIterations, maxTabu, maxCandidates, timeLimit)

def solveSimAnneal(tsp, startTemp, endTemp, iterations, printUpdateFreq = 100):
	sim = SimulatedAnnealing(tsp)
	sim.Tmin = endTemp
	sim.Tmax = startTemp
	sim.steps = iterations
	sim.updates = printUpdateFreq

	route, cost = sim.anneal()
	return route

def solveGrasp(tsp, maxNoImprovements, maxIterations, alpha, timeLimit):
	return grasp.search(tsp, maxIterations, maxNoImprovements, alpha, timeLimit)

def solveGenetic(tsp, generations):
	genetic = Genetic(tsp)

	for i in range(0, generations):
		genetic.nextGeneration()

	return genetic.entirePopulation[genetic.minIndex]

def solveAntColony(tsp, antCount, iterations, repetitions):
	try:
		graph = AntGraph(tsp)
		bestPath = None
		bestCost = sys.maxsize
		for i in range(0, repetitions):
			graph.reset_tau()
			colony = AntColony(graph, antCount, iterations)
			colony.start()
			if colony.best_path_cost < bestCost:
				bestPath = colony.best_path_vec
				bestCost = colony.best_path_cost

		return bestPath

	except Exception as e:
		print("exception: " + str(e))