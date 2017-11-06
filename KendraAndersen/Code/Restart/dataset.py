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

# This function takes one transmitter's location in a grid of width x_max
# and height y_max, then computes received power at all points for a 
# particular wavelength
def received_power_grid(wavelength, xy_max, xy_transmit):
	X = np.arange(0,xy_max[0],1)
	Y = np.arange(0,xy_max[1],1)
	X, Y = np.meshgrid(X, Y)
	d = np.sqrt((xy_transmit[0]-X)**2 + (xy_transmit[1]-Y)**2)
	P_r = np.log10(wavelength/(4*pi*d))*20
	return P_r

# This function takes the output from received_power_grid and plots it
# in a figure as numbered. 
def plot_received_power(received_power, n=1): 
	plt.figure(n)
	colors = ['red','orange','yellow','green']
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
			for x in range(0, xy_coords[i+1][0]-xy_coords[i][0]):
				path_power.append(received_power[xy_coords[i][0]+x,xy_coords[i][1]])
		# if vertical path
		if xy_coords[i+1][1] != xy_coords[i][1]:
			for y in range(0, xy_coords[i+1][1]-xy_coords[i][1]):
				path_power.append(received_power[xy_coords[i][0],xy_coords[i][1]+y])
	return path_power

# Testing the functions
# Setup: Grid 100x100, frequency 2.4 GHz -> wavelength = c/f = 122.45 mm
# 		 Multiple transmitters at different locations
field_size = [100, 100]
Transmitters = [[50,50],[25,25],[25,75],[100,100]]
received_power = [None]*len(Transmitters)
for i, transmitter in enumerate(Transmitters):
	received_power[i] = received_power_grid(0.12245, field_size, transmitter)
max_received_power = np.maximum.reduce(received_power)

# Plot the results by color (red is weakest, green is strongest)
plot_received_power(max_received_power)
plt.title('Maximum Received Power for Several Transmitters')
for i, transmitter in enumerate(Transmitters):
	plot_received_power(received_power[i], 2+i)
	title = 'Received Power of Transmitter at '+str(transmitter)
	plt.title(title)

# Create a path and plot the received power over it
# Assume only vertical and horizontal paths for now
path = [[0,0],[0,50],[50,50],[50,100]]
path_power = [None]*len(Transmitters)
plt.figure(6)
legend = [None]*len(Transmitters)
for i, transmitter in enumerate(Transmitters):
	path_power[i] = received_power_over_path(received_power[i], path)
	plt.plot(path_power[i])
	legend[i] = str(transmitter)
# plt.plot(received_power_over_path(max_received_power, path))
# legend.append('Max')
plt.legend(legend, title='Transmitters at:')
plt.title('Received Power over Specified Path')
plt.ylabel('Received Power (dB)')
plt.xlabel('Distance Along Path (m)')
plt.show()