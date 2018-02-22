# Author: Kendra Andersen
# Huff Research Group
# Created: 02/16/18

# This file, test_simulated_data.py, applies the modified Dijkstra algorithm
# to the simulated data and plots it. 

# Import modules
from data_import import *
from dijkstar import Graph, find_path

# Import data for Horn Antenna at 900 MHz @ Engineering Quad
path_powers = [None]*3
path_coordinates = [None]*3
path_powers[0], path_coordinates[0] = get_path_data(1)
path_powers[1], path_coordinates[1] = get_path_data(2)
path_powers[2], path_coordinates[2] = get_path_data(3)

# Plot data for Horn Antenna at 900 Mhz @ Engineering Quad
plot_power_over_sim_path(path_powers[0], title='Power Over Path 1', n=1)
plot_power_over_sim_path(path_powers[1], title='Power Over Path 2', n=2)
plot_power_over_sim_path(path_powers[2], title='Power Over Path 3', n=3)

# # Create a graph for implementing Dijkstra's
# graph = Graph()
# graph.add_edge(1,2,{'path':1})
# graph.add_edge(1,2,{'path':2})
# graph.add_edge(1,2,{'path':3})
# # Other direction of edges: 
# graph.add_edge(2,1,{'path':1})
# graph.add_edge(2,1,{'path':2})
# graph.add_edge(2,1,{'path':3})

# # Define the cost function
# cost_func_tx1 = lambda u, v, e, prev_e: -sum(path_powers[e['path']-1][0])
# cost_func_tx2 = lambda u, v, e, prev_e: -sum(path_powers[e['path']-1][1])
# cost_func_tx4 = lambda u, v, e, prev_e: -sum(path_powers[e['path']-1][3])

# # Find the best path using Dijkstra's
# # I think there's an error since we have identical nodes. 
# shortest_path_tx1 = find_path(graph,1,2,cost_func=cost_func_tx1)
# print("Path maximizing Tx1:")
# print(str(shortest_path_tx1[1])+" Cost: "+str(shortest_path_tx1[3]))
# shortest_path_tx2 = find_path(graph,1,2,cost_func=cost_func_tx2)
# print("Path maximizing Tx2:")
# print(str(shortest_path_tx2[1])+" Cost: "+str(shortest_path_tx2[3]))
# #It'd be reasonable to get a different answer for Tx4
# shortest_path_tx4 = find_path(graph,1,2,cost_func=cost_func_tx4)
# print("Path maximizing Tx4:")
# print(str(shortest_path_tx4[1])+" Cost: "+str(shortest_path_tx4[3]))

# Convert to optimization function from data_import:
best_path_tx1 = find_best_path_for_tx(path_powers, 0)
plot_tx_over_paths(path_powers, 0, 'Power over Paths for Tx1', n=4)
best_path_tx2 = find_best_path_for_tx(path_powers, 1)
plot_tx_over_paths(path_powers, 1, 'Power over Paths for Tx2', n=5)
best_path_tx4 = find_best_path_for_tx(path_powers, 3)
plot_tx_over_paths(path_powers, 3, 'Power over Paths for Tx4', n=6)

# What about the best SNR? 
best_path_tx1_tx2 = find_best_path_for_SNR(path_powers,0,1)
plot_SNR_over_paths(path_powers, 0, 1, 'SNR (Tx1/Tx2) over Paths', n=8)

# Plot the path coordinates so we have an idea of their configurations
plot_paths(path_coordinates, n=7)
plt.show()
