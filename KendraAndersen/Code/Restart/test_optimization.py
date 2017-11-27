# Author: Kendra Andersen
# Huff Research Group
# Created: 11/26/17

# This script, test_optimization.py, tests the functions defined. 

from data_creation import *
from optimization import *

# Setting up the data to test the optimization through: 
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

# Create a path and plot the received power over it
# Assume only vertical and horizontal paths for now
rss_of_paths = []
path_powers = []
path1 = [[0,0],[0,50],[50,50],[50,100]]
path_power1, rss1 = plot_power_over_path(path1, Transmitters, received_power, n=6, title='Received Power over Path 1')
path_powers.append(path_power1)
rss_of_paths.append(rss1)

# Create another path and plot the received power over it
# Assume only vertical and horizontal paths for now
path2 = [[99,0],[99,50],[50,50],[50,100]]
path_power2, rss2 = plot_power_over_path(path2, Transmitters, received_power, n=7, title='Received Power over Path 2')
path_powers.append(path_power2)
rss_of_paths.append(rss2)

# Test the above functions to see if their results match intuition. 
# The path with the strongest signal from the transmitter at [25,25]
# should be Path 1
path_maximizing_t(1, Transmitters, rss_of_paths)
# If the good transmitter is at [27,75] and the bad transmitter is at [50,50],
# Path 1 should have stronger signal from the good transmitter and both 
# should have equal signal from the noise transmitter. Thus Path 1 optimizes
# the SNR ratio. 
optimize_ratio(2, 0, Transmitters, rss_of_paths)

# Plot the ratio of good to bad over the paths
plot_ratio_over_paths([path1,path2], path_powers, 2, 0, n=8)

plt.show()