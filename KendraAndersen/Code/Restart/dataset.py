# Author: Kendra Andersen
# Huff Research Group
# Created: 11/3/17

# Friis Transmission Equation with decibels is 
# P_r = P_t + D_t + D_r + 20*log(lambda/(4*pi*d))
# 	P_r is power at the receiver in dB
# 	P_t is power delivered to the terminals of the transmitter in dB
# 	D_t is the directivity of the transmitter in dBi
#	D_r is the directivity of the receiver in dBi
#	lambda is the wavelength of the receiver
#	d is the distance between the antennas
# For reference: https://en.wikipedia.org/wiki/Friis_transmission_equation

# This code will generate a dataset of P_r given the location of the transmitter
# Assumptions: 
#	- P_t = 0
#	- D_t = 0 (omnidirectional transmitter)
#	- D_r = 0 (omnidirectional receiver)
# Thus Friis simplifies to:
# P_r = 20*log(lambda/(4*pi*d))

# Import libraries
from math import *
import matplotlib.pyplot as plt 
import matplotlib as mpl
import numpy as np
from dijkstar import Graph, find_path

# This function takes one transmitter's location in a grid of width x_max
# and height y_max, then computes received power at all points for a 
# particular wavelength
def received_power_grid(wavelength, xy_max, xy_transmit):
	X = np.arange(0,xy_max[0],1)
	Y = np.arange(0,xy_max[1],1)
	X, Y = np.meshgrid(X, Y)
	d = np.sqrt((xy_transmit[0]-X)**2 + (xy_transmit[1]-Y)**2)
	P_r = np.log10(wavelength/(4*pi*d))*20
	bools = np.isinf(P_r)
	for xindex,yrow in enumerate(bools): 
		for yindex,b in enumerate(yrow): 
			if b == True: 
				P_r[xindex][yindex] = 0
	return P_r

# This function takes the output from received_power_grid and plots it
# in a figure as numbered. 
def plot_received_power(received_power, n=1): 
	plt.figure(n)
	colors = ['purple','red','orange','yellow','yellowgreen','green','green','black']
	cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', colors, 256)
	img = plt.imshow(received_power, interpolation='nearest', cmap=cmap, origin='lower')
	plt.colorbar(img, cmap=cmap, label='Received Power (dB)')
	plt.ylabel('Y Coordinate (m)')
	plt.xlabel('X Coordinate (m)')

# This function takes the output from received_power_grid and a series
# of (x,y) coordinates and returns an array of received_power over the 
# path traced by the coordinates.
# The coordinates must describe vertical or horizontal path segments.
def received_power_over_path(received_power, xy_coords): 
	path_power = []
	for i in range(0, len(xy_coords) - 1): 
		# if horizontal path
		if xy_coords[i+1][0] != xy_coords[i][0]:
			step_size_x = 1 if xy_coords[i+1][0]>xy_coords[i][0] else -1
			for x in range(0, xy_coords[i+1][0]-xy_coords[i][0], step_size_x):
				path_power.append(received_power[xy_coords[i][0]+x,xy_coords[i][1]])
		# if vertical path
		if xy_coords[i+1][1] != xy_coords[i][1]:
			step_size_y = 1 if xy_coords[i+1][1]>xy_coords[i][1] else -1
			for y in range(0, xy_coords[i+1][1]-xy_coords[i][1], step_size_y):
				path_power.append(received_power[xy_coords[i][0],xy_coords[i][1]+y])
	return path_power

# This function takes a path, set of transmitters, the received power from the
# transmitters, a plot title, and figure number, and plots the received
# power curves from each transmitter as well as returning the average RSS from
# each transmitter over the specified path. 
def plot_power_over_path(path, Transmitters, received_power, title='Received Power over Specified Path', n=1):
	path_power = [None]*len(Transmitters)
	path_rss = [None]*len(Transmitters)
	plt.figure(n)
	legend = [None]*len(Transmitters)
	for i, transmitter in enumerate(Transmitters):
		path_power[i] = received_power_over_path(received_power[i], path)
		plt.plot(path_power[i])
		legend[i] = str(transmitter)
		path_rss[i] = sum(path_power[i]*1)/len(path_power[i])
	plt.legend(legend, title='Transmitters at:')
	plt.title(title)
	plt.ylabel('Received Power (dB)')
	plt.xlabel('Distange Along Path (m)')
	return path_power, path_rss

# This function takes a list of paths and the power of various transmitters
# over the path. It then plots the ratio of good power/bad power for each
# point on the paths. 
def plot_ratio_over_paths(paths, path_powers, good_index, bad_index, n=1):
	plt.figure(n)
	legend = [None]*len(paths)
	for i, path in enumerate(paths):
		ratio = np.array(path_powers[i][good_index])/np.array(path_powers[i][bad_index])
		plt.plot(ratio)
		legend[i] = 'Path '+str(i+1)
	plt.title('SNR Over Specified Paths')
	plt.ylabel('Signal/Noise Ratio')
	plt.xlabel('Distance Along Path (m)')
	plt.legend(legend)

# Testing the functions
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
# Create am individual plot for each transmitter
# for i, transmitter in enumerate(Transmitters):
# 	plot_received_power(received_power[i], 2+i)
# 	title = 'Received Power of Transmitter at '+str(transmitter)
# 	plt.title(title)

# # Create a path and plot the received power over it
# # Assume only vertical and horizontal paths for now
# rss_of_paths = []
# path_powers = []
# path1 = [[0,0],[0,50],[50,50],[50,100]]
# path_power1, rss1 = plot_power_over_path(path1, Transmitters, received_power, n=6, title='Received Power over Path 1')
# path_powers.append(path_power1)
# rss_of_paths.append(rss1)

# # Create another path and plot the received power over it
# # Assume only vertical and horizontal paths for now
# path2 = [[99,0],[99,50],[50,50],[50,100]]
# path_power2, rss2 = plot_power_over_path(path2, Transmitters, received_power, n=7, title='Received Power over Path 2')
# path_powers.append(path_power2)
# rss_of_paths.append(rss2)

# # STILL TO DO: Figure out non-horizontal or vertical paths!
# # We can plot them though:
# # path3 = [[0,0],[50,50],[50,100]]

# # Plot the paths on the maximum power color plot. 
# # This needs to become a function eventually. 
# plt.figure(1)
# p = []
# p.append(plt.plot(*zip(*path1)))
# p.append(plt.plot(*zip(*path2)))
# # p.append(plt.plot(*zip(*path3)))
# plt.setp(p, linestyle='--')
# plt.legend(['Path 1','Path 2','Path 3'])
# plt.gca().set_xlim([0,field_size[0]])
# plt.gca().set_ylim([0,field_size[1]])

# Now to move on to the optimization problem. 

# This function compares the average SNR over several paths for a good
# transmitter and bad transmitter. It then prints its decision as to which
# path maximizes the SNR and returns the path number. 
def optimize_ratio(good_index, bad_index, Transmitters, rss_of_paths):
# def optimize_ratio(good_transmitter, bad_transmitter, Transmitters, rss_of_paths):
# 	# Find the index of the transmitters
# 	for index,t in enumerate(Transmitters):
# 		if t == good_transmitter:
# 			good_index = index
# 		if t == bad_transmitter:
# 			bad_index = index
	# Find the ratio of good/bad for each path
	ratios_by_path = []
	for path in rss_of_paths: 
		ratios_by_path.append(path[good_index]/path[bad_index])
	best_path_index = np.argmax(ratios_by_path)
	print('For good transmitter '+str(Transmitters[good_index])+' and bad transmitter '+str(Transmitters[bad_index])+',')
	print('Path '+str(best_path_index+1)+' maximizes the ratio of good/bad received power.')
	return best_path_index+1

# This function compares the signal strength from a transmitter for each
# path and decides which path has the strongest signal for that transmitter, 
# returning the path number. 
def path_maximizing_t(transmitter_index, rss_of_paths):
	transmitter_rss_by_path = []
	for path in rss_of_paths:
		transmitter_rss_by_path.append(path[transmitter_index])
	index = np.argmax(transmitter_rss_by_path)
	print('Path '+str(index+1)+' maximizes received power from the transmitter at '+str(Transmitters[transmitter_index]))
	return index+1

# # Test the above functions to see if their results match intuition. 
# # The path with the strongest signal from the transmitter at [25,25]
# # should be Path 1
# path_maximizing_t(1,rss_of_paths)
# # If the good transmitter is at [27,75] and the bad transmitter is at [50,50],
# # Path 1 should have stronger signal from the good transmitter and both 
# # should have equal signal from the noise transmitter. Thus Path 1 optimizes
# # the SNR ratio. 
# optimize_ratio(2, 0, Transmitters, rss_of_paths)

# # Plot the ratio of good to bad over the paths
# plot_ratio_over_paths([path1,path2], path_powers, 2, 0, n=8)

# Now, to add Dijkstra's into the mix. 
# Instead of separate paths, we're going to have path segments which we
# integrate over to get their 'cost'. We then apply dijkstra's to get the
# best path. 
# Start with a simple T layout
# seg1 = [[50,0],[50,40]]
# seg2 = [[50,40],[0,40]]
# seg3 = [[50,40],[100,40]]
# I'm having issues with transmitter at [27,75] having the wrong plots of power
# So this is the temporary output fix. FIND THE ISSUE AND RESOLVE THIS!!
seg1 = [[0,50],[40,50]]
seg1p = [[50,0],[50,40]]
seg2 = [[40,50],[40,100]]
seg2p = [[50,40],[100,40]]
seg3 = [[40,50],[40,0]]
seg3p = [[50,40],[0,40]]
seg4 = [[0,50],[0,0],[40,0]]
seg4p = [[50,0],[0,0],[0,40]]

# Plot the segments on the maximum power color plot. 
# This needs to become a function eventually. 
plt.figure(1)
p = []
p.append(plt.plot(*zip(*seg1p)))
p.append(plt.plot(*zip(*seg2p)))
p.append(plt.plot(*zip(*seg3p)))
p.append(plt.plot(*zip(*seg4p), color="yellow"))
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