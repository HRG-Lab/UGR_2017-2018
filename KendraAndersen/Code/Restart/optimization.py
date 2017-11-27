# Author: Kendra Andersen
# Huff Research Group
# Created: 11/26/17

# This file, optimization.py, defines a series of functions useful for the 
# optimization problem. 

import numpy as np

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
	best_path_index = np.argmin(ratios_by_path)
	print('For good transmitter '+str(Transmitters[good_index])+' and bad transmitter '+str(Transmitters[bad_index])+',')
	print('Path '+str(best_path_index+1)+' maximizes the ratio of good/bad received power.')
	return best_path_index+1

# This function compares the signal strength from a transmitter for each
# path and decides which path has the strongest signal for that transmitter, 
# returning the path number. 
def path_maximizing_t(transmitter_index, Transmitters, rss_of_paths):
	transmitter_rss_by_path = []
	for path in rss_of_paths:
		transmitter_rss_by_path.append(path[transmitter_index])
	index = np.argmax(transmitter_rss_by_path)
	print('Path '+str(index+1)+' maximizes received power from the transmitter at '+str(Transmitters[transmitter_index]))
	return index+1