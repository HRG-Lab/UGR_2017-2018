# Author: Kendra Andersen
# Last Updated: 10/24/17
# Huff Research Group

from dijkstar import Graph, find_path
from dijkstar.algorithm import single_source_shortest_paths, extract_shortest_path_from_predecessor_list
# graph = Graph()

# # Add edges to graph: these are paths between nodes. 
# # Need to find a way to automate this for large graphs
# # Edges are only in one direction!
# graph.add_edge(1, 2, {'cost': 1})
# graph.add_edge(2, 3, {'cost': 2})
# graph.add_edge(1, 4, {'cost': 2})
# graph.add_edge(4, 3, {'cost': 1})
# # Other direction of edges
# graph.add_edge(2, 1, {'cost': 1})
# graph.add_edge(3, 2, {'cost': 2})
# graph.add_edge(4, 1, {'cost': 2})
# graph.add_edge(3, 4, {'cost': 1})

# Alternate graph setup:
graph = Graph({
	1: {2:1, 4:2},
	2: {1:1, 3:2},
	3: {2:2, 4:1},
	4: {1:2, 3:2}
	})

# Define the cost function
# cost_func = lambda u, v, e, prev_e: e['cost']
# arguments are u, v, e, and prev_e
# the expression is e['cost']

# Now find the shortest path from 1 to 3 and from 3 to 1
# path1 = find_path(graph, 1, 3, cost_func = cost_func)
# path2 = find_path(graph, 3, 1, cost_func = cost_func)
path1 = find_path(graph, 1, 3)
path2 = find_path(graph, 3, 1)
print(path1)
print(path2)
print("Path 1: " + str(path1[0]) + " Cost: " + str(path1[3]))
print("Path 2: " + str(path2[0]) + " Cost: " + str(path2[3]))

# Get a list of shortest distance between start and point i
disS = [0] * 5
for i in range(1,5):
	# disS[i] = find_path(graph, 1, i, cost_func = cost_func)[3]
	disS[i] = find_path(graph, 1, i)[3]
print(disS)

# Get a list of shortest distance between end an point i
disT = [0] * 5
for i in range(1,5):
	# disT[i] = find_path(graph, i, 3, cost_func = cost_func)[3]
	disT[i] = find_path(graph, i, 3)[3]
print(disT)

# Testing another provided algorithm
predecessors = single_source_shortest_paths(graph, 1)
print(predecessors)
print(extract_shortest_path_from_predecessor_list(predecessors, 3))
# This is the shortest path from source node (1) to all other nodes??

