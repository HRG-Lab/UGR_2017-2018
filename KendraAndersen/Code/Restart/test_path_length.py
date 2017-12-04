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
x = 60
seg1 = [[40,0],[40,20]]
seg2 = [[40,20],[40,30]]
seg3 = [[40,30],[40,80]]
seg4 = [[40,20],[90,20]]
seg5 = [[40,30],[75,30]]
seg6 = [[40,80],[x,80]]
seg7 = [[x,80],[75,80]]
seg8 = [[75,80],[90,80]]
seg9 = [[x,80],[x,100]]
seg10 = [[75,30],[75,80]]
seg11 = [[90,20],[90,80]]
segments = [seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11]

# Plot the segments on the maximum power color plot. 
plot_segments(segments, field_size)
# Label the Nodes
nodes_x = [40,40,40,40,90,75,x,75,90,x]
nodes_y = [0,20,30,80,20,30,80,80,80,100]
# nodes_x = [40,40,75,75,0,100,40,75,0,40,75,100]
# nodes_y = [0,30,0,30,30,30,80,80,80,100,100,80]
plot_nodes(nodes_x,nodes_y)

# Now we create the graph for implementing Dijkstra's
graph = Graph()

graph.add_edge(1,2,{'seg':1})
graph.add_edge(2,3,{'seg':2})
graph.add_edge(3,4,{'seg':3})
graph.add_edge(2,5,{'seg':4})
graph.add_edge(3,6,{'seg':5})
graph.add_edge(4,7,{'seg':6})
graph.add_edge(7,8,{'seg':7})
graph.add_edge(8,9,{'seg':8})
graph.add_edge(7,10,{'seg':9})
graph.add_edge(6,8,{'seg':10})
graph.add_edge(5,9,{'seg':11})
# Other direction of edges: 
graph.add_edge(2,1,{'seg':1})
graph.add_edge(3,2,{'seg':2})
graph.add_edge(4,3,{'seg':3})
graph.add_edge(5,2,{'seg':4})
graph.add_edge(6,3,{'seg':5})
graph.add_edge(7,4,{'seg':6})
graph.add_edge(8,7,{'seg':7})
graph.add_edge(9,8,{'seg':8})
graph.add_edge(10,7,{'seg':9})
graph.add_edge(8,6,{'seg':10})
graph.add_edge(9,5,{'seg':11})

# Get the costs & power over the segments
segments_powers = plot_seg_power(segments, Transmitters, received_power)

# Define the cost function
# cost_func = lambda u, v, e, prev_e: e['cost']
# cost_func0 = lambda u, v, e, prev_e: -segments_cost1[e['seg']-1]
cost_func0 = lambda u, v, e, prev_e: -sum(segments_powers[e['seg']-1][1])
cost_func1 = lambda u, v, e, prev_e: -sum(segments_powers[e['seg']-1][3])

# Find the best path from 1 to 10
shortest_path0 = find_path(graph,1,10,cost_func=cost_func0)
print("Path from Node 1 to Node 10 maximizing transmitter at [25,25]:")
print("Path: " +str(shortest_path0[0])+" Cost: "+str(shortest_path0[3]))
shortest_path1 = find_path(graph,1,10,cost_func=cost_func1)
print("Path from Node 1 to Node 10 maximizing transmitter at [100,50]:")
print("Path: "+str(shortest_path1[0])+" Cost: "+str(shortest_path1[3]))

# SNR Ratios: Just the one for this example
rssi_grid2= received_power[3]/received_power[1]
plot_rss_ratio(rssi_grid2, n=6)
plt.title("SNR of Transmitter at [100,50]/Transmitter at [25,25]")
plot_segments(segments, field_size, n=6)
plot_nodes(nodes_x,nodes_y,n=6)

segments_snr1 = [None]*len(segments_powers)
for i, seg in enumerate(segments_powers):
	segments_snr1[i] = np.array(segments_powers[i][3])/np.array(segments_powers[i][1])
cost_func3 = lambda u, v, e, prev_e: sum(segments_snr1[e['seg']-1])
shortest_path3 = find_path(graph,1,10,cost_func=cost_func3)
print("Path from Node 1 to Node 10 maximizing SNR of [100,50]/[25,25]:")
print("Path: "+str(shortest_path3[0])+" Cost: "+str(shortest_path3[3]))

# Two Good, one noisy source:
rssi_grid3 = received_power[1]/received_power[2]
rssi_grid4 = received_power[3]/received_power[2]
rssis = np.array([rssi_grid3,rssi_grid4])
max_rssi_grid = np.minimum.reduce(rssis)
plot_rss_ratio(max_rssi_grid,n=7)
plt.title("SNR with Two Good Transmitters and One Noisy")
plot_segments(segments, field_size, n=7)
plot_nodes(nodes_x,nodes_y,n=7)

segments_snrmax = [None]*len(segments_powers)
for i, seg in enumerate(segments_powers):
	value1 = np.array(segments_powers[i][1])/np.array(segments_powers[i][2])
	value2 = np.array(segments_powers[i][3])/np.array(segments_powers[i][2])
	segments_snrmax[i] = np.minimum.reduce(np.array([value1, value2]))
cost_func4 = lambda u, v, e, prev_e: sum(segments_snrmax[e['seg']-1])
shortest_path4 = find_path(graph, 1, 10, cost_func=cost_func4)
print("Path form Node 1 to Node 10 maximizing SNR with two good and one noisy:")
print("Path: "+str(shortest_path4[0])+" Cost: "+str(shortest_path4[3]))

# Check my answers
path1 = [[40,0],[40,20],[40,30],[40,80],[x,80],[x,100]]
title1 = 'Received Power over Path 1 [1,2,3,4,7,10]'
path2 = [[40,0],[40,20],[40,30],[75,30],[75,80],[x,80],[x,100]]
title2 = 'Received Power over Path 2 [1,2,3,6,8,7,10]'
path3 = [[40,0],[40,20],[90,20],[90,80],[75,80],[x,80],[x,100]]
title3 = 'Received Power over Path 3 [1,2,5,9,8,7,10]'
path1_power, rss1 = plot_power_over_path(path1,Transmitters,received_power,n=3,title=title1,ylim=[-80,-60])
path2_power, rss2 = plot_power_over_path(path2,Transmitters,received_power,n=4,title=title2,ylim=[-80,-60])
path3_power, rss3 = plot_power_over_path(path3,Transmitters,received_power,n=5,title=title3,ylim=[-80,-60])

# Implement prioritization of path length vs. signal strength
cost_func5 = lambda u, v, e, prev_e: -sum(np.array(segments_powers[e['seg']-1][3])**7)
shortest_path5 = find_path(graph,1,10,cost_func=cost_func5)
print("Path from Node 1 to Node 10 strongly maximizing transmitter at [100,50]:")
print("Path: "+str(shortest_path5[0])+" Cost: "+str(shortest_path5[3]))

plt.figure(10)
plt.plot(np.array(path1_power[3])**7)
plt.plot(np.array(path2_power[3])**7)
plt.plot(np.array(path3_power[3])**7)
plt.legend(["Path 1","Path 2","Path 3"])
plt.title("Received Power ^ 7 from Transmitter at [100,50]")

plt.figure(11)
plt.plot(path1_power[3])
plt.plot(path2_power[3])
plt.plot(path3_power[3])
plt.legend(["Path 1","Path 2","Path 3"])
plt.title("Received Power from Transmitter at [100,50]")

plt.figure(12)
plt.plot(np.array(path1_power[3])**99)
plt.plot(np.array(path2_power[3])**99)
plt.plot(np.array(path3_power[3])**99)
plt.legend(["Path 1","Path 2","Path 3"])
plt.title("Received Power ^ 99 from Transmitter at [100,50]")

plt.show()	