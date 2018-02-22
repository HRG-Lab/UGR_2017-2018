# Author: Kendra Andersen
# Huff Research Group
# Created: 02/16/18

# This file, data_setup.py, defines a series of functions useful for 
# importing, plotting, and organizing data. 

# Import modules
import numpy as np
import matplotlib.pyplot as plt

# This function allows for automatic generation of the directory information of the 
# specified data, following naming conventions established by Sarah. 
def get_directory_name(path, tx):
	# Start with the folder housing all of the data
	name = "C:/Users/Kendralyn/Documents/Programs/git/UGR_2017-2018/KendraAndersen/Data/"
	# Add folder for frequency & configuration
	name = name + "EngineeringQuadHorn900/"
	# Create the file name using conventions & specified values
	name = name + "EQ_1_H_Rx"
	name = name + str(path)
	name = name + "_900 MHz_Tx"
	name = name + str(tx)
	name = name + ".p2m"
	return name 

# This function returns two arrays, the first is the power over the specified path
# while the second is the XYZ coordinates of the specified path. Each point on the
# path is 5m apart.  
def get_path_data(path):
	# Data order: Index, X(m), Y(m), Z(m), Distance(m), Power(dBm), Phase(deg)
	# We'll ignore distance & phase. Each point is 5m apart. 
	path_1_power = [None]*5
	path_1_coordinates = [None]*3
	index,path_1_coordinates[0],path_1_coordinates[1],path_1_coordinates[2],d,path_1_power[0],p = np.loadtxt(get_directory_name(path,1),skiprows=2,unpack=True)
	index,x,y,z,d,path_1_power[1],p = np.loadtxt(get_directory_name(path,2),skiprows=2,unpack=True)
	index,x,y,z,d,path_1_power[2],p = np.loadtxt(get_directory_name(path,3),skiprows=2,unpack=True)
	index,x,y,z,d,path_1_power[3],p= np.loadtxt(get_directory_name(path,4),skiprows=2,unpack=True)
	index,x,y,z,d,path_1_power[4],p = np.loadtxt(get_directory_name(path,5),skiprows=2,unpack=True)

	# Return the datax
	return path_1_power, path_1_coordinates

# This function plots the powers from several transmitters over the specified path. 
# It requires an array of the power over the path and returns a plot. 
def plot_power_over_sim_path(path_power, title='Transmitter Powers over Specified Path', n=1, ylim=[-250,0]):
	plt.figure(n)
	legend = [None]*len(path_power)
	for i, tx in enumerate(path_power):
		plt.plot(tx)
		legend[i] = "Tx" + str(i+1)
	plt.legend(legend)
	plt.title(title)
	plt.ylabel('Power (dBm)')
	plt.xlabel('Distance Along Path (5m)')
	plt.gca().set_ylim(ylim)

# This function plots the powers over several paths for a specific transmitter. 
# It requires an array of the powers over all paths and the index of the transmitter. 
# It will plot the power for each path. 
def plot_tx_over_paths(path_powers, tx, title='Power Over Paths for Specified Transmitter', n=1, ylim=[-250,0]):
	plt.figure(n)
	legend = [None]*len(path_powers)
	for i, path in enumerate(path_powers):
		plt.plot(path[tx])
		legend[i] = "Path " + str(i+1)
	plt.legend(legend)
	plt.title(title)
	plt.ylabel('Power (dBm)')
	plt.xlabel('Distance Along Path (5m)')
	plt.gca().set_ylim(ylim)

# This function plots the SNR of two transmitters over the paths. 
def plot_SNR_over_paths(path_powers, tx_signal, tx_noise, title='SNR Over Paths', n=1):
	plt.figure(n)
	legend = [None]*len(path_powers)
	for i, path in enumerate(path_powers):
		plt.plot(path[tx_signal]/path[tx_noise])
		legend[i] = "Path " + str(i+1)
	plt.legend(legend)
	plt.title(title)
	plt.ylabel('SNR')
	plt.xlabel('Distance Along Path (5m)')


# This function plots the XY coordinates of the paths on a coordinate plane. 
# It requires an array of the coordinates arranged as X, Y. 
def plot_paths(path_coordinates, title='Engineering Quad Paths', n=1):
	plt.figure(n)
	legend = [None]*len(path_coordinates)
	for i, path in enumerate(path_coordinates): 
		plt.plot(path[0],path[1])
		legend[i] = "Path " + str(i+1)
	plt.legend(legend)
	plt.title(title)
	plt.ylabel('Y Coordinate (m)')
	plt.xlabel('X Coordinate (m)')

# This function returns the index for the path which has the strongest signal
# from the transmitter specified by tx. 
def find_best_path_for_tx(path_powers, tx):
	cost = []
	for path in path_powers: 
		cost.append(-sum(path[tx]))
	lowest_cost_index = np.argmin(cost)
	print('Path '+str(lowest_cost_index+1)+' maximizes power from Tx'+str(tx+1))
	return lowest_cost_index

# This function returns the index for the path which has the best SNR ratio
# for the specified noisy and good transmitters
def find_best_path_for_SNR(path_powers, tx_signal, tx_noise):
	cost = []
	for path in path_powers: 
		# rss_signal = sum(path[tx_signal])/(5*len(path[tx_signal]))
		# rss_noise = sum(path[tx_noise])/(5*len(path[tx_noise]))
		cost.append(-sum(path[tx_signal]/path[tx_noise]))
	lowest_cost_index = np.argmin(cost)
	print('Path '+str(lowest_cost_index+1)+' maximizes SNR of Tx'+str(tx_signal+1)+'/Tx'+str(tx_noise+1))
	return lowest_cost_index