# Author: Kendra Andersen
# Huff Research Group
# Created: 11/26/17

# This file, graph_definition.py, defines a series of functions useful for 
# arranging and plotting graphs. 

import matplotlib.pyplot as plt 
from data_creation import *

# This function plots a series of linear segments of the input plot, given a list of 
# segments of the format [[x1,y1],[x2,y2]] , the field size, and a figure number.  
def plot_segments(segments, field_size, n=1):
	plt.figure(n)
	ax = plt.subplot(111)
	p = []
	legend = [None]*len(segments)
	for i,seg in enumerate(segments):
		p.append(plt.plot(*zip(*seg)))
		legend[i] = 'Segment ' + str(i+1)
	plt.setp(p, linestyle='--')
	# Put the legend underneath
	ax = plt.subplot(111)
	box = ax.get_position()
	ax.set_position([box.x0, box.y0+box.height*0.2, box.width, box.height*0.8])
	plt.legend(legend, bbox_to_anchor=(0.5,-0.15), loc='upper center', ncol=3)
	plt.gca().set_xlim([-1,field_size[0]])
	plt.gca().set_ylim([-1,field_size[1]])

def plot_nodes(nodes_x, nodes_y, n=1):
	plt.figure(n)
	plt.scatter(nodes_x,nodes_y,color='black')
	for i in range(0, len(nodes_x)):
		label = str(i+1)
		plt.annotate(label,xy=[nodes_x[i],nodes_y[i]],xytext=(5,-5),textcoords='offset points')

def plot_seg_power(segments, good_index, Transmitters, received_power, n=2):
	segments_powers = [None]*len(segments)
	segments_rss = [None]*len(segments)
	for i,seg in enumerate(segments):
		title = 'Received Power over Segment ' + str(i+1)
		segments_powers[i], segments_rss[i] = plot_power_over_path(seg,Transmitters,received_power,n=n+i,title=title,plot_on=0)
	return segments_powers

