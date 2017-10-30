# Utilities

from collections import defaultdict, deque

def vertexCost(tsp, index):
	sumValue = 0

	for i in range(0, tsp.getSize()):
		sumValue += tsp.getCost(i, index)
		sumValue += tsp.getCost(index, i)

	# 2 times as many costs as points
	return sumValue/(tsp.getSize()*2)

def buildVertexCosts(tsp):
	costs = numpy.array(tsp.getSize())

	for city in range(0, tsp.getSize()):
		costs[city] = vertexCost(tsp, city)

	return costs



class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


# From Gist https://gist.github.com/mdsrosa/c71339cb23bc51e711d8
def dijkstra(tsp, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(range(tsp.getSize()))

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for second_node in range(tsp.getSize()):
            try:
                weight = current_weight + tsp.getCost(min_node, second_node)
            except:
                continue
            if second_node not in visited or weight < visited[second_node]:
                visited[second_node] = weight
                path[second_node] = min_node

    return visited, path


def dijkstraShortestPath(tsp, origin, destination):
    visited, paths = dijkstra(tsp, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)