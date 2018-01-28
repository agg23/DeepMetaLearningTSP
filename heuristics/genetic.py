#This is an alternative attempt at implementing a TSP algorithm using a genetic algorithm
#While it functions, it is often bogged down in local minima/premature convergence, and hence
#was not chosen as the tournament TSP algorithm for our team
from solver.utilities import generateInitialSolution, calculateCost
import numpy
import random
import math
import sys

class Genetic(object):

	def __init__(self, tsp, mutationRate, populationSize):
		self.tsp = tsp
		# Defaults to 10
		self.mutationRate = mutationRate
		# Defaults to 800
		self.populationSize = populationSize #s/b 100,000
		self.groupSize = 10 #must be >= 5
		self.entirePopulation = numpy.empty((self.populationSize, self.tsp.getSize()), dtype = int)
		self.entirePopulationLengths = numpy.empty(self.populationSize)
		self.minDistance = None
		self.minIndex = None

		self.crossoverGroup = numpy.empty((self.groupSize, self.tsp.getSize()), dtype = int)
		self.crossoverIndices = numpy.empty(self.groupSize, dtype = int)

		self.crossoverGroupTourLengths = numpy.empty(self.groupSize)

		for i in range(0, self.populationSize):
			tour = generateInitialSolution(tsp)
			self.entirePopulation[i] = tour
			self.entirePopulationLengths[i] = calculateCost(tour, self.tsp)

	# def printPopulation(self):
	#     for i in range(0, len(self.entirePopulation)):
	#         print(self.entirePopulation[i].getCities())

	# def printOptimalTour(self, outputFileName):
	#     out = open(outputFileName, 'w')
	#     out.write(str(self.minDistance) + "\n")
	#     minTour = list(self.entirePopulation[self.minIndex].getCities())

	#     for i in range(0, len(minTour)):
	#         out.write(str(minTour[i][0]) + "\n")

	def printDistances(self):
		for i in range(0, len(self.entirePopulation)):
			print(self.entirePopulation[i].getDistance())

	def mutate(self, perm, mutationRate):
		if(random.randint(0,100) < mutationRate):
			a = random.randint(0, self.tsp.getSize() - 1)
			b = random.randint(0, self.tsp.getSize() - 1)

			perm[a], perm[b] = perm[b], perm[a]

		return perm

	def nextGeneration(self):
		for i in range(0, self.groupSize):
			index = numpy.random.randint(0, self.populationSize - 1)

			self.crossoverIndices[i] = index

			self.crossoverGroupTourLengths[i] = self.entirePopulationLengths[index]
			self.crossoverGroup[i] = self.entirePopulation[index]

		self.sortCrossoverGroup()

		parentSelect = self.determineParents()
		children = crossover(self.tsp, self.crossoverGroup[parentSelect[0]], self.crossoverGroup[parentSelect[1]])

		child1Index = self.crossoverIndices[self.groupSize - 2]
		child2Index = self.crossoverIndices[self.groupSize - 1]

		#set the lowest two tours to the crossovered children
		self.entirePopulation[child1Index] = children[0]
		self.entirePopulation[child2Index] = children[1]

		#attempt to mutate the children
		self.entirePopulation[child1Index] = self.mutate(self.entirePopulation[child1Index], self.mutationRate)
		self.entirePopulation[child2Index] = self.mutate(self.entirePopulation[child2Index], self.mutationRate)

		#update the distance of the children
		child1Cost = calculateCost(self.entirePopulation[child1Index], self.tsp)
		child2Cost = calculateCost(self.entirePopulation[child2Index], self.tsp)

		self.entirePopulationLengths[child1Index] = child1Cost
		self.entirePopulationLengths[child2Index] = child2Cost

		self.updateDistance(child1Index, child1Cost)
		self.updateDistance(child2Index, child2Cost)

	#determine parents based on a group size of 5 or more
	#creates crossover from at least 1 of the two shortest distance tours
	#attempts to maintain diversity somewhat by ocassionaly incorporating lower-quality parents for crossover,
	#though at a less frequent level
	def determineParents(self):
		parentRandom = random.randrange(0,100)

		if(parentRandom <= 40):
			return 0, 1
		elif(parentRandom <=60):
			return 0, 2
		elif(parentRandom <= 70):
			return 0, self.groupSize - 2
		elif(parentRandom <= 80):
			return 0, self.groupSize - 1
		elif(parentRandom <= 90):
			return 1, 2
		elif(parentRandom <= 95):
			return 1, self.groupSize - 2
		elif(parentRandom < 100):
			return 1, self.groupSize - 1

	def updateDistance(self, tourIndex, cost):
		if(self.minDistance == None or self.minDistance > cost):
			self.minDistance = cost
			self.minIndex = tourIndex

	#insertion sort crossover group
	def sortCrossoverGroup(self):
		# print(crossoverGroup)
		# crossoverGroup.sort(key = lambda group: calculateCost(group[1], self.tsp))
		sortedTourIndices = numpy.argsort(self.crossoverGroupTourLengths)
		# print(sortedTourIndices)
		self.crossoverGroup = self.crossoverGroup[sortedTourIndices]

#Using Partially Mapped Crossover
def crossover(tsp, parent1, parent2):
	# create two crossover points
	tourLength = tsp.getSize()
	a = numpy.random.randint(0, tourLength - 1)
	b = numpy.random.randint(a, tourLength)
	# create two empty lists for the children
	child1 = numpy.full(tourLength, -1, dtype=int)
	child2 = numpy.full(tourLength, -1, dtype=int)

	child1Cities = set()
	child2Cities = set()

	# copy the crossover elements
	for i in range(a, b):
		child1[i] = parent2[i]
		child1Cities.add(parent2[i])
		child2[i] = parent1[i]
		child2Cities.add(parent1[i])

	for i in range(0, tourLength):
		if (child1[i] == -1 and parent1[i] not in child1Cities):
			child1[i] = parent1[i]
			child1Cities.add(parent1[i])
		if (child2[i] == -1 and parent2[i] not in child2Cities):
			child2[i] = parent2[i]
			child2Cities.add(parent2[i])
	parent1Curr = a
	parent2Curr = a

	# fills the empty spaces with any non-duplicates from the cities that were crossed over
	for i in range(0, tourLength):
		if (child1[i] == -1):
			while (child1[i] == -1 and parent1Curr < b):
				if (parent1[parent1Curr] not in child1Cities):
					child1[i] = parent1[parent1Curr]
					child1Cities.add(parent1[parent1Curr])

				parent1Curr += 1

		if (child2[i] == -1):
			while (child2[i] == -1 and parent2Curr < b):
				if (parent2[parent2Curr] not in child2Cities):
					child2[i] = parent2[parent2Curr]
					child2Cities.add(parent2[parent2Curr])

				parent2Curr += 1

	return child1, child2
