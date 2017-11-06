# Author: Kendra Andersen
# Huff Research Group

from dijkstar import Graph, find_path

graph = Graph()

# Add edges to graph
graph.add_edge(1, 2, {'length': 1}, {'rss': 0.75})
graph.add_edge(2, 3, {'length': 2}, {'rss': 0.5})
graph.add_edge(1, 4, {'length': 2}, {'rss': 0.5})
graph.add_edge(4, 3, {'length': 1}, {'rss': 0.25})
# Other direction of edges
graph.add_edge(2, 1, {'length': 1}, {'rss': 0.75})
graph.add_edge(3, 2, {'length': 2}, {'rss': 0.5})
graph.add_edge(4, 1, {'length': 2}, {'rss': 0.5})
graph.add_edge(3, 4, {'length': 1}, {'rss': 0.25})

# Define the cost function
def cost_func(u, v, e, prev_e):
	# Do it by average RSSI
	return (prev_e['length'] + e['length'])/(prev_e['length']/prev_e['rss'] + e['length']/e['rss'])
# This won't work. The costs are added up in the comparison, but I need a different function. 