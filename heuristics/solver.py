import sys
import time

import heuristics.tabu as tabu
import heuristics.grasp as grasp
from .simanneal import SimulatedAnnealing
from .genetic import Genetic

from .antcolony import AntColony
from .antgraph import AntGraph

def time_string(seconds):
	"""Returns time in seconds as a string formatted HHHH:MM:SS."""
	s = int(round(seconds))  # round to nearest second
	h, s = divmod(s, 3600)   # get hours and remainder
	m, s = divmod(s, 60)     # split remainder into minutes and seconds
	return '%4i:%02i:%02i' % (h, m, s)

# From simanneal module
def printUpdate(firstTitle, firstValue, energy, accept, improve, startTime, totalIterations):
	elapsed = time.time() - startTime

	if firstValue == 0:
		print('%s        Energy    Accept   Improve     Elapsed   Remaining'
			% (firstTitle), file=sys.stderr)
		print('\r%12d  %12.2f                      %s            ' %
			(firstValue + 1, sys.maxsize, time_string(elapsed)), file=sys.stderr, end="\r")
		sys.stderr.flush()
	else:
		remain = (totalIterations - firstValue) * (elapsed / firstValue)
		print('\r%12d  %12.2f  %7.2f%%  %7.2f%%  %s  %s\r' %
			  (firstValue + 1, energy, accept, improve,
			   time_string(elapsed), time_string(remain)), file=sys.stderr, end="\r")
		sys.stderr.flush()

def solveTabu(tsp, maxCandidates, maxTabu, maxIterations, timeLimit):
	updateLambda = lambda firstValue, energy, accept, improve, startTime, totalIterations: printUpdate("   Iteration", firstValue, energy, accept, improve, startTime, totalIterations)
	return tabu.search(tsp, maxIterations, maxTabu, maxCandidates, timeLimit, updateLambda)

def solveSimAnneal(tsp, startTemp, endTemp, iterations, printUpdateFreq = 100):
	sim = SimulatedAnnealing(tsp)
	sim.Tmin = endTemp
	sim.Tmax = startTemp
	sim.steps = iterations
	sim.updates = printUpdateFreq

	route, cost = sim.anneal()
	return route

def solveGrasp(tsp, maxNoImprovements, maxIterations, alpha, timeLimit):
	updateLambda = lambda firstValue, energy, accept, improve, startTime, totalIterations: printUpdate("   Iteration", firstValue, energy, accept, improve, startTime, totalIterations)
	return grasp.search(tsp, maxIterations, maxNoImprovements, alpha, timeLimit, updateLambda)

def solveGenetic(tsp, generations):
	start = time.time()

	genetic = Genetic(tsp)

	for i in range(0, generations):	
		# TODO: Add accept and improve
		printUpdate("  Generation", i, genetic.minDistance, 100.0 * 1, 100.0 * 1, start, generations)
		
		genetic.nextGeneration()

	return genetic.entirePopulation[genetic.minIndex]

def solveAntColony(tsp, antCount, iterations, repetitions):
	try:
		graph = AntGraph(tsp)
		bestPath = None
		bestCost = sys.maxsize
		for i in range(0, repetitions):
			graph.reset_tau()
			updateLambda = lambda firstValue, energy, accept, improve, startTime: printUpdate("   Iteration", firstValue + i * iterations, energy, accept, improve, startTime, iterations * repetitions)
			colony = AntColony(graph, antCount, iterations, updateLambda)
			colony.start()
			if colony.best_path_cost < bestCost:
				bestPath = colony.best_path_vec
				bestCost = colony.best_path_cost

		return bestPath

	except Exception as e:
		print("exception: " + str(e))