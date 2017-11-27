# Author: Kendra Andersen
# Huff Research Group
# Created: 11/26/17

# This file, data_creation.py, provides a set of functions used to create a RF
# environment test dataset. 

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

def plot_rss_ratio(rss, n=1):
	plt.figure(n)
	colors = ['black','green','green','yellowgreen','yellow','orange','red','purple']
	cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', colors, 256)
	img = plt.imshow(rss, interpolation='nearest', cmap=cmap, origin='lower')
	plt.colorbar(img, cmap=cmap, label='SNR (dB/dB)')
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
				path_power.append(received_power[xy_coords[i][1],xy_coords[i][0]+x])
		# if vertical path
		if xy_coords[i+1][1] != xy_coords[i][1]:
			step_size_y = 1 if xy_coords[i+1][1]>xy_coords[i][1] else -1
			for y in range(0, xy_coords[i+1][1]-xy_coords[i][1], step_size_y):
				path_power.append(received_power[xy_coords[i][1]+y,xy_coords[i][0]])
	return path_power

# This function takes a path, set of transmitters, the received power from the
# transmitters, a plot title, and figure number, and plots the received
# power curves from each transmitter as well as returning the average RSS from
# each transmitter over the specified path. 
def plot_power_over_path(path, Transmitters, received_power, title='Received Power over Specified Path', n=1, plot_on=1, ylim=[0,0]):
	path_power = [None]*len(Transmitters)
	path_rss = [None]*len(Transmitters)
	if plot_on == 1: 
		plt.figure(n)
		legend = [None]*len(Transmitters)
	for i, transmitter in enumerate(Transmitters):
		path_power[i] = received_power_over_path(received_power[i], path)
		if plot_on == 1: 
			plt.plot(path_power[i])
			legend[i] = str(transmitter)
		path_rss[i] = sum(path_power[i]*1)/len(path_power[i])
	if plot_on == 1: 
		plt.legend(legend, title='Transmitters at:')
		plt.title(title)
		plt.ylabel('Received Power (dB)')
		plt.xlabel('Distange Along Path (m)')
		if ylim != [0,0]:
			plt.gca().set_ylim(ylim)
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