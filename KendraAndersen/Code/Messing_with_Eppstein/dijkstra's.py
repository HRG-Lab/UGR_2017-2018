# Author: Kendra Andersen
# Huff Resesarch Group

# Modifying Dijkstra's algorithm so that instead of computing the shortest path, 
# we are computing the shadiest path (that is sufficiently short). 

from priodict import priorityDictionary

def Dijkstra(G, start, end = None): 
	# dictionary of final distances
	D = {}
	# dictionalry of predecessors
	P = {}
	# estimated distances of non-final vertices
	Q = priorityDictionary()
	Q[start] = 0

	for v in Q: 
		D[v] = Q[v]
		if v == end: 
			break

		for w in G[v]: 
			vwLength = D[v] + G[v][w]
			if w in D: 
				if vwLength < D[w]: 
					raise ValueError("Dijkstra: found better path to already-final vertex")
				elif w not in Q or vwLength < Q[w]: 
					Q[w] = vwLength
					P[w] = v
	return (D, P)

def shortestPath(G, start, end):
	D, P = Dijkstra(G, start, end)
	Path = []
	while 1: 
		Path.append(end)
		if end == start: 
			break
		end = P[end]
	Path.reverse()
	return Path

# example
# This means node s connects to u with length 10, x with length 5, etc. 
G = {'s': {'u':10, 'x':5},
	'u': {'v':1, 'x':2},
	'v': {'y':4},
	'x': {'u':3, 'v':9, 'y':2},
	'y': {'s':7,'v':6}}
print(Dijkstra(G,'s'))
print(shortestPath(G,'s','v'))