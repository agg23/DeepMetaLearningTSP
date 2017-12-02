from operator import itemgetter
import numpy

def min_spanning_tree(graph):
	"""
	input graph is a dictionary mapping ordered pairs to their edge weight.
	return value is a subset of the input graph, consisting of the edges
	in the minimum spanning tree
	"""
	vertex_set = [v for e in graph.keys() for v in e]
	vertex_set = list(set(vertex_set))

	# sort the edges by weight
	edge_set = graph.items()
	edge_set = sorted(edge_set, key=itemgetter(1))

	# for each vertex, maintain the smallest vertex in it's component. To start, 
	# the graph has no edges, so each vertex is in it's own component
	min_vertex_in_component = {v:v for v in vertex_set}
	tree = {}
	index = 0
	while len(tree)<len(vertex_set)-1:
		edge, weight = edge_set[index]
		x,y = edge
		if min_vertex_in_component[x] != min_vertex_in_component[y]:
			tree[edge] = weight
			new_min = min(min_vertex_in_component[x], min_vertex_in_component[y])
			old_min = max(min_vertex_in_component[x], min_vertex_in_component[y])
			for v in vertex_set:
				if min_vertex_in_component[v] == old_min:
					min_vertex_in_component[v] = new_min
		index += 1

	return tree

def smallest_two_edges(graph):
	"""
	returns the two edges with minimum weight
	"""
	min_edge_1, min_edge_2 = max(graph.values()), 
	for edge in graph:
		if graph[edge] <= graph[min_edge_1]:
			min_edge_1, min_edge_2 = edge, min_edge_1
		elif graph[edge] < graph[min_edge_2]:
			min_edge_2 = edge
	return min_edge_1, min_edge_2

def min_one_tree(graph):
	"""
	input graph is a dictionary mapping ordered pairs to their edge weight.
	return value is a subset of the input graph, consisting of the edges
	in the minimum 1-tree
	"""

	# choose the 1-vertex to be the smallest
	vertex_set = [v for e in graph.keys() for v in e]
	vertex_set = list(set(vertex_set))
	one_vertex = min(vertex_set)

	# find the min spanning tree of the graph without the 1-vertex
	subgraph = {e:graph[e] for e in graph if not one_vertex in e}
	one_tree = min_spanning_tree(subgraph)

	# add the 2 edges adjacent to the 1-vertex of min weight into the one_tree
	adj_edges = {e:graph[e] for e in graph if one_vertex in e}
	for i in range(2):
		min_edge, min_weight = min(adj_edges.items(), key=itemgetter(1))
		one_tree[min_edge] = min_weight
		del adj_edges[min_edge]

	return one_tree

def adjust_weights(graph, one_tree, stepsize):
	"""
	Checks if the 1-tree is a tour, and if not, adjusts the graph weights according to 
	the stepsize. 
	Returns a boolean and a graph. If the Boolean is true, then the 1-tree is a tour, and
	the graph is the input graph. If the Boolean is false, then the 1-tree is not a tour
	and the graph is the graph with adjusted weights.
	"""

	# Get the degrees of each vertex
	vertex_set = [v for e in graph.keys() for v in e]
	vertex_set = list(set(vertex_set))
	degree = dict()
	for v in vertex_set:
		degree[v] =  sum([(v in edge) for edge in one_tree])

	# Check if the 1-tree is a tour
	if min(degree.values()) == 2 and max(degree.values())==2:
		return True, graph

	#make graph of new weights
	adjusted_graph = dict()
	for edge in graph:
		# ideally the sum of the degrees of the vertices in this edge will be 4.
		# increase (decrease) the weight by stepsize for each degree that it is
		# deficient (over)
		edge_degree = degree[edge[0]] + degree[edge[1]]
		adjusted_graph[edge] = graph[edge] + stepsize*(edge_degree-4)

	return False, adjusted_graph

def tspToDict(tsp):
	"""
	For convience's sake, converts TSP instance into graph dictionary format used by Held-Karp implementation.
	Inefficient, but saves development time
	"""
	graph = {}

	n = tsp.getSize()
	for x in range(n):
		for y in range(n):
			if not tsp.getAdjacent(x, y):
				continue

			graph[(x, y)] = tsp.getCost(x, y)

	return graph

def findLowerBound(tsp, alpha=1.0, beta=.95, times=100, maxTimes=100):

	"""
	This function uses the held-karp 1-tree method to find a lower
	bound on the weight of a hamiltonian tour graph. 

	The stepsize in the algorithm is /alpha/. When an iteration doesn't
	increase the lower bound, we decrease the stepsize by a factor of 
	/beta/. Once we have /times/ iterations in a row without increasing
	the lower bound, we terminate the algorithm.
	"""

	graph = tspToDict(tsp)

	iterations_without_increase = 0
	prev_max = 0
	#iterate
	iterations = 0
	while iterations_without_increase < times and iterations < maxTimes:

		# meat of held-karp: 
		# find the minimum spanning 1-tree and update edge weights
		# accordingly
		one_tree = min_one_tree(graph)
		weight = sum(one_tree.values())
		optimal, graph = adjust_weights(graph, one_tree, alpha)

		# housekeeping:
		# update the max, the stepsize, and the running count of 
		# iterations without an increase to the max.
		if optimal:
			break
		if weight > prev_max:
			prev_max = weight
			iterations_without_increase = 0
		else:
			alpha *= beta
			iterations_without_increase += 1

		iterations += 1

	# get the weight in terms of the original graph
	return weight
