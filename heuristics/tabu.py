'''
Strategy
The strategy is to restrict the return to newly visited areas of space
of search through a heuristic incorporated to the algorithm (cyclically).
The algorithm maintains a small memory of recent steps and prevents
to undo those changes. This strategy can be extended
adding intermediate memory structures to serve as biases in
steps closer to the promising areas (intensification), as well as
long-term memory to promote diversity.

Heuristic
The Tabu Search was designed to manage a heuristic
can be adapted to manage any heuristic exploration of neighborhood.

It has been predominantly applied to discrete domains, such as
combinatorial optimization.

Candidates for neighboring steps can be generated
neighborhood, or the neighborhood can be sampled stochastically at a
fixed size, exchanging efficiency for accuracy.
'''
from solver.utilities import generateInitialSolution, calculateCost
import time
import numpy
import random

def stochasticTwoOptWithEdges(perm):
    result = numpy.copy(perm)
    size = result.shape[0]
    p1, p2 = random.randrange(0,size), random.randrange(0,size)
    exclude = set([p1])
    if p1 == 0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)

    if p1 == size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1)

    while p2 in exclude:
        p2 = random.randrange(0,size)

    if p2<p1:
        p1, p2 = p2, p1

    result[p1:p2] = numpy.flipud(result[p1:p2])

    return result, [[perm[p1-1],perm[p1]],[perm[p2-1],perm[p2]]]

# Function that returns the best candidate, ordered by cost
def locateBestCandidate(candidates):
    # TODO: Modify to not sort
    candidates.sort(key=lambda c: c["candidate"]["cost"])
    best, edges = candidates[0]["candidate"], candidates[0]["edges"]
    return best, edges


def isTabu(perm, tabuList, timeLimit):
    if time.time() > timeLimit:
        return False
    count = 0
    count += 1
    result = False
    size = len(perm)
    for index, edge in enumerate(perm):
        if index == size - 1:
            edge2 = perm[0]
        else:
            edge2 = perm[index + 1]
        if [edge, edge2] in tabuList:
            result = True
            break

    return result


def generateCandidates(best, tabuList, tsp, timeLimit):
    permutation, edges, result = [], None, {}
    while len(permutation) < 1 or isTabu(best["permutation"], tabuList, timeLimit):
        permutation, edges = stochasticTwoOptWithEdges(best["permutation"])
    candidate = {}
    candidate["permutation"] = permutation
    candidate["cost"] = calculateCost(candidate["permutation"], tsp)
    result["candidate"] = candidate
    result["edges"] = edges
    return result


def search(tsp, maxIterations, maxTabu, maxCandidates, timeLimit):
    t_end = time.time() + timeLimit
    # construct a random tour
    best = {}
    best["permutation"] = generateInitialSolution(tsp)
    best["cost"] = calculateCost(best["permutation"], tsp)
    tabuList = []
    while maxIterations > 0 and time.time() < t_end:
        # Generates queries using the local search 2-opt algorithm
        # stochastically, near the best candidate of this iteration.
        # Uses the tabu list not to visit vertices more than once
        candidates = []
        for index in range(0, maxCandidates):
            candidates.append(generateCandidates(best, tabuList, tsp, t_end))
        # Find the best candidate
        # sorts the list of candidates by cost
        bestCandidate, bestCandidateEdges = locateBestCandidate(candidates)
        # compares with the best candidate and updates it if necessary
        if bestCandidate["cost"] < best["cost"]:
            # defines the current candidate as the best
            best = bestCandidate
            # Update the taboo list
            for edge in bestCandidateEdges:
                if len(tabuList) < maxTabu:
                    tabuList.append(edge)
        maxIterations -= 1

        return best

def searchIteration(tsp, maxIterations, maxTabu, maxCandidates, timeLimit):
    t_end = time.time() + timeLimit
    best_list = []
    # builds the initial solution
    best = {}
    best["permutation"] = generateInitialSolution(tsp)
    best["cost"] = calculateCost(best["permutation"], tsp)
    tabuList = []
    while maxIterations > 0 and time.time() < t_end:
        # Generates queries using the local search 2-opt algorithm
        # stochastically, near the best candidate of this iteration.
        # Uses the tabu list not to visit vertices more than once
        candidates = []
        for index in range(0, maxCandidates):
            candidates.append(generateCandidates(best, tabuList, tsp, t_end))
        # Find the best candidate
        # sorts the list of employees by cost
        bestCandidate, bestCandidateEdges = locateBestCandidate(candidates)
        # compares with the best candidate and updates it if necessary
        if bestCandidate["cost"] < best["cost"]:
            # defines the current candidate as the best
            best = bestCandidate
            # Update the taboo list
            for edge in bestCandidateEdges:
                if len(tabuList) < maxTabu:
                    tabuList.append(edge)
        maxIterations -= 1
        best_list.append(best["cost"])

    return best_list