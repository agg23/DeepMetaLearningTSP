def generateInitialSolution(tsp):
	size = tsp.getSize()

	solution = np.arange(size)

	for index in range(size):
		randomIndex = random.randrange(index, size)
		temp = solution[index]
		solution[index] = solution[randomIndex]
		solution[randomIndex] = temp

	return solution