# Author: Kendra Andersen
# Huff Research Group
# Created: 11/26/17

# This script, test_data_creation.py, uses the functions created in data_creation.py
# to create a series of plots. 

from data_creation import *

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
for i, transmitter in enumerate(Transmitters):
	plot_received_power(received_power[i], 2+i)
	title = 'Received Power of Transmitter at '+str(transmitter)
	plt.title(title)

# Create a path and plot the received power over it
# Assume only vertical and horizontal paths for now
# rss_of_paths = []
# path_powers = []
path1 = [[0,0],[0,50],[50,50],[50,100]]
path_power1, rss1 = plot_power_over_path(path1, Transmitters, received_power, n=6, title='Received Power over Path 1')
# path_powers.append(path_power1)
# rss_of_paths.append(rss1)

# Create another path and plot the received power over it
# Assume only vertical and horizontal paths for now
path2 = [[99,0],[99,50],[50,50],[50,100]]
path_power2, rss2 = plot_power_over_path(path2, Transmitters, received_power, n=7, title='Received Power over Path 2')
# path_powers.append(path_power2)
# rss_of_paths.append(rss2)

# STILL TO DO: Figure out non-horizontal or vertical paths!
# We can plot them though:
path3 = [[0,0],[50,50],[50,100]]

# Plot the paths on the maximum power color plot. 
# This needs to become a function eventually. 
plt.figure(1)
p = []
p.append(plt.plot(*zip(*path1)))
p.append(plt.plot(*zip(*path2)))
# p.append(plt.plot(*zip(*path3)))
plt.setp(p, linestyle='--')
plt.legend(['Path 1','Path 2','Path 3'])
plt.gca().set_xlim([0,field_size[0]])
plt.gca().set_ylim([0,field_size[1]])

plt.show()