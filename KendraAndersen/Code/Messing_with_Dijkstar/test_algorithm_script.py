from dijkstar import find_path, NoPathError, Graph
from dijkstar.algorithm import single_source_shortest_paths

graph = Graph({'a': {'b': 10, 'c': 100, 'd': 1},'b': {'c': 10},'d': {'b': 1, 'e': 1},'e': {'f': 1},})
graph.add_node('f', {'c': 1})
graph['f'] = {'c': 1}

graph.add_edge('f', 'c', 1)
graph.add_edge('g', 'b', 1)

nodes = list(graph)
nodes.sort()

incoming = graph.get_incoming('c')
incoming_nodes = list(incoming.keys())
incoming_nodes.sort()

paths = single_source_shortest_paths(graph, 'a')
print(paths)