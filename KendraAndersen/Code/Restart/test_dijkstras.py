# Author: Kendra Andersen
# Huff Research Group
# Created: 11/26/17

# This script, test_dijkstras.py, tests the previously defined functions in the context
# of using Dijkstra's Algorithm. 

from data_creation import *
from optimization import *
from dijkstar import Graph, find_path

# Setup: Grid 100x100, frequency 2.4 GHz -> wavelength = c/f = 122.45 mm
# 		 Multiple transmitters at different locations
field_size = [100, 100]
t0 = [50,50]
t1 = [25,25]
t2 = [27,75]
t3 = [100,100]
Transmitters = [t0,t1,t2,t3]
received_power = [None]*len(Transmitters)
for i, transmitter in enumerate(Transmitters):
	received_power[i] = received_power_grid(0.12245, field_size, transmitter)
max_received_power = np.maximum.reduce(received_power)

# Plot the results by color (purple is weakest, black is strongest)
plot_received_power(max_received_power)
plt.title('Maximum Received Power for Several Transmitters')

# Instead of separate paths, we're going to have path segments which we
# integrate over to get their 'cost'. We then apply dijkstra's to get the
# best path. 
# Start with a simple T layout
# seg1 = [[50,0],[50,40]]
# seg2 = [[50,40],[0,40]]
# seg3 = [[50,40],[100,40]]
# I'm having issues with transmitter at [27,75] having the wrong plots of power
# So this is the temporary output fix. FIND THE ISSUE AND RESOLVE THIS!!
seg1 = [[50,0],[50,40]]
seg2 = [[50,40],[100,40]]
seg3 = [[50,40],[0,40]]
seg4 = [[50,0],[0,0],[0,40]]

# Plot the segments on the maximum power color plot. 
# This needs to become a function eventually. 
plt.figure(1)
p = []
p.append(plt.plot(*zip(*seg1)))
p.append(plt.plot(*zip(*seg2)))
p.append(plt.plot(*zip(*seg3)))
p.append(plt.plot(*zip(*seg4), color="yellow"))
plt.setp(p, linestyle='--')
plt.legend(['Segment 1','Segment 2','Segment 3','Segment 4'])
plt.gca().set_xlim([-1,field_size[0]])
plt.gca().set_ylim([-1,field_size[1]])

# Find the power and RSS over these segments:
seg_power1, srss1 = plot_power_over_path(seg1, Transmitters, received_power, n=9, title='Received Power over Segment 1')
seg_power2, srss2 = plot_power_over_path(seg2, Transmitters, received_power, n=10, title='Received Power over Segment 2')
seg_power3, srss3 = plot_power_over_path(seg3, Transmitters, received_power, n=11, title='Received Power over Segment 3')
seg_power4, srss4 = plot_power_over_path(seg4, Transmitters, received_power, n=12, title='Received Power over Segment 4')

# Determine the 'cost' of each segment
# First case: only maximizing power from transmitter at [25,25], index 1. 
# Seg 1 is 40 units long, so it has the smallest cost (-2764)
cost1 = sum(seg_power1[1])
# Seg 2 and 3 are both 50 units long, they have costs of (-3710) and (-3310) respectively.
# Seg 3 would be best choice to max this transmitter, and it has a less negative number. 
cost2 = sum(seg_power2[1])
cost3 = sum(seg_power3[1])
# So negate these numbers and we have the costs for Dijkstra's algorithm. 
# Seg 4 is 90 units long, it has the largest cost of (-6231)
cost4 = sum(seg_power4[1])
print(cost1,cost2,cost3,cost4)

# Now implement dijkstra's: 
# Start by establishing the graph. This needs to be automated somehow. 
graph = Graph()
# Add paths between nodes. Their cost is negated so it's positive. 
# Node 1: [50,0]; Node 2: [50 ,40]
# Node 3: [0,40]; Node 4: [100,40]
graph.add_edge(1,2,{'cost':-cost1})
graph.add_edge(2,3,{'cost':-cost3})
graph.add_edge(2,4,{'cost':-cost2})
graph.add_edge(1,3,{'cost':-cost4})
# Other direction of edges:
graph.add_edge(2,1,{'cost':-cost1})
graph.add_edge(3,2,{'cost':-cost3})
graph.add_edge(4,2,{'cost':-cost2})
graph.add_edge(3,1,{'cost':-cost4})

# Define the cost function
cost_func = lambda u, v, e, prev_e: e['cost']

# Find the shortest path from 1 to 3
shortest_path1 = find_path(graph,1,3, cost_func=cost_func)
print("Path from [50,0] to [0,40]")
print("Shortest Path 1: "+str(shortest_path1[0])+" Cost: "+str(shortest_path1[3]))

# Label the Nodes
plt.figure(1)
plt.scatter([50,50,0,100],[0,40,40,40],color='black')
for i, xy in enumerate([[50,0],[50,40],[0,40],[100,40]]):
	label = 'Node '+str(i+1)
	plt.annotate(label, xy=xy, xytext=(-20,5), textcoords='offset points')

plt.show()