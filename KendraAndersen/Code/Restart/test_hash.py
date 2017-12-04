# Author: Kendra Andersen
# Huff Research Group
# Created: 11/26/17

# This script, test_hash.py, tests the previously defined functions in the context
# of using Dijkstra's Algorithm on a hash path structure.

from data_creation import *
from optimization import *
from graph_definition import *
from dijkstar import Graph, find_path

# Setup: Grid 100x100, frequency 2.4 GHz -> wavelength = c/f = 122.45 mm
#        Multiple transmitters at different locations
field_size = [100, 100]
t0 = [50,50]
t1 = [25,25]
t2 = [27,75]
t3 = [100,50]
Transmitters = [t0,t1,t2,t3]
received_power = [None]*len(Transmitters)
for i, transmitter in enumerate(Transmitters):
	received_power[i] = received_power_grid(0.12245, field_size, transmitter)
max_received_power = np.maximum.reduce(received_power)

# Plot the results by color (purple is weakest, black is strongest)
plot_received_power(max_received_power)
plt.title('Maximum Received Power for Several Transmitters')

# We'll have a series of path segments which we get costs from. 
# They are laid out in a hash pattern.
seg1 = [[40,0],[40,30]]
seg2 = [[75,0],[75,30]]
seg3 = [[40,30],[75,30]]
seg4 = [[40,30],[0,30]]
seg5 = [[75,30],[100,30]]
seg6 = [[40,30],[40,80]]
seg7 = [[75,30],[75,80]]
seg8 = [[40,80],[75,80]]
seg9 = [[40,80],[0,80]]
seg10 = [[40,80],[40,100]]
seg11 = [[75,80],[75,100]]
seg12 = [[75,80],[100,80]]
segments = [seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11, seg12]

# Plot the segments on the maximum power color plot. 
plot_segments(segments, field_size)
# Label the Nodes
nodes_x = [40,40,75,75,0,100,40,75,0,40,75,100]
nodes_y = [0,30,0,30,30,30,80,80,80,100,100,80]
plot_nodes(nodes_x,nodes_y)

# Now we create the graph for implementing Dijkstra's
graph = Graph()

graph.add_edge(1,2,{'seg':1})
graph.add_edge(3,4,{'seg':2})
graph.add_edge(2,4,{'seg':3})
graph.add_edge(2,5,{'seg':4})
graph.add_edge(4,6,{'seg':5})
graph.add_edge(2,7,{'seg':6})
graph.add_edge(4,8,{'seg':7})
graph.add_edge(7,8,{'seg':8})
graph.add_edge(7,9,{'seg':9})
graph.add_edge(7,10,{'seg':10})
graph.add_edge(8,11,{'seg':11})
graph.add_edge(8,12,{'seg':12})
# Other direction of edges: 
graph.add_edge(2,1,{'seg':1})
graph.add_edge(4,3,{'seg':2})
graph.add_edge(4,2,{'seg':3})
graph.add_edge(5,2,{'seg':4})
graph.add_edge(6,4,{'seg':5})
graph.add_edge(7,2,{'seg':6})
graph.add_edge(8,4,{'seg':7})
graph.add_edge(8,7,{'seg':8})
graph.add_edge(9,7,{'seg':9})
graph.add_edge(10,7,{'seg':10})
graph.add_edge(11,8,{'seg':11})
graph.add_edge(12,8,{'seg':12})

# Get the costs & power over the segments
# This time, we're getting the cost of the transmitter at [25,25], index 1
segments_powers = plot_seg_power(segments, 1, Transmitters, received_power)

# Define the cost function
# cost_func = lambda u, v, e, prev_e: e['cost']
# cost_func0 = lambda u, v, e, prev_e: -segments_cost1[e['seg']-1]
cost_func0 = lambda u, v, e, prev_e: -sum(segments_powers[e['seg']-1][1])
cost_func1 = lambda u, v, e, prev_e: -sum(segments_powers[e['seg']-1][3])

# Find the shortest path from 1 to 11
shortest_path0 = find_path(graph,1,11,cost_func=cost_func0)
print("Path from Node 1 to Node 11 maximizing transmitter at [25,25]:")
print("Path: " +str(shortest_path0[0])+" Cost: "+str(shortest_path0[3]))
shortest_path1 = find_path(graph,1,11,cost_func=cost_func1)
print("Path from Node 1 to Node 11 maximizing transmitter at [100,50]:")
print("Path: "+str(shortest_path1[0])+" Cost: "+str(shortest_path1[3]))

# Now what if we were dealing with SNR ratios? 
# Make a plot where we put the values of good signal/bad signal, good signal is [50,50],
# index 0, and bad signal is [25,25], index 1
rssi_grid = received_power[0]/received_power[1]
plot_rss_ratio(rssi_grid, n=2)
plt.title("SNR of Transmitter at [50,50]/Transmitter at [25,25]")
plot_segments(segments, field_size, n=2)
plot_nodes(nodes_x,nodes_y,n=2)

# Then test out dijkstra's on it. Do SNR because it tries to MINIMIZE the area 
# under the curve. 
segments_snr0 = [None]*len(segments_powers)
for i,seg in enumerate(segments_powers):
	segments_snr0[i] = np.array(segments_powers[i][0])/np.array(segments_powers[i][1])
cost_func2 = lambda u, v, e, prev_e: sum(segments_snr0[e['seg']-1])
shortest_path2 = find_path(graph,1,11,cost_func=cost_func2)
print("Path from Node 1 to Node 11 maximizing SNR of [50,50]/[25,25]:")
print("Path: "+str(shortest_path2[0])+" Cost: "+str(shortest_path2[3]))

# Another case to test: 
rssi_grid2 = received_power[3]/received_power[1]
plot_rss_ratio(rssi_grid2, n=6)
plt.title("SNR of Transmitter at [100,50]/Transmitter at [25,25]")
plot_segments(segments, field_size, n=6)
plot_nodes(nodes_x,nodes_y,n=6)

segments_snr1 = [None]*len(segments_powers)
for i, seg in enumerate(segments_powers):
	segments_snr1[i] = np.array(segments_powers[i][3])/np.array(segments_powers[i][1])
cost_func3 = lambda u, v, e, prev_e: sum(segments_snr1[e['seg']-1])
shortest_path3 = find_path(graph,1,11,cost_func=cost_func3)
print("Path from Node 1 to Node 11 maxmizing SNR of [100,50]/[25,25]:")
print("Path: "+str(shortest_path3[0])+" Cost: "+str(shortest_path3[3]))

# Check my answers
path1 = [[40,0],[40,30],[40,80],[75,80],[75,100]]
title1 = 'Received Power over Path 1 [1,2,7,8,11]'
path2 = [[40,0],[40,30],[75,30],[75,80],[75,100]]
title2 = 'Received Power over Path 2 [1,2,4,8,11]'
path1_power, rss1 = plot_power_over_path(path1,Transmitters,received_power,n=3,title=title1,ylim=[-85,-55])
path2_power, rss2 = plot_power_over_path(path2,Transmitters,received_power,n=4,title=title2,ylim=[-85,-55])
plot_ratio_over_paths([path1,path2],[path1_power,path2_power],0,1,n=5)
plot_ratio_over_paths([path1,path2],[path1_power,path2_power],3,1,n=7)

plt.show()