# Author: Kendra Andersen
# Huff Research Group
# Created: 02/14/18

# This file, map_definition.py, defines a series of functions useful for 
# arranging and plotting data on maps. 

# Import libraries
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt 

# Try again
# Lambert conformal map of US lower 48 states
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_1=33,lat_2=45,lon_0=-95,resolution='h',area_thresh=10000)
# Draw coastlines and boundaries
m.drawcoastlines()
m.drawcountries(linewidth=2)
m.drawstates()
# Fill in colors
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
# Parallels and Meridians
m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
# Title and plot
plt.title('USA')

# Create Basemap instance 
# map = Basemap(width=12000,height=9000,projection='lcc',resolution=None,lat_0=50,lon_0=-107)
# map=Basemap(width=1200,height=900,projection='lcc',resolution=None,lat_1=30.615,lat_2=30.635,lat_0=30.625,lon_0=-96.338)
# map.bluemarble(scale=0.5)
# # Draw coastlines & boundaries
# map.drawcoastlines()
# map.drawmapboundary(fill_color='aqua')
# map.fillcontinents(color='coral',lake_color='aqua')
# map.drawstates()
# map.drawcountries()
# # Draw parallels and meridians
# map.drawparallels(np.arange(0.,90,10.))
# map.drawmeridians(np.arange(180.,360.,10.))
# # Add title and show plot
# plt.title('map')
plt.show() 