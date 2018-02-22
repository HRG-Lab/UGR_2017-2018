# Author: Kendra Andersen
# Huff Research Group
# Created: 12/04/17

# This script, test_mysql.py, obtains data from a mysql database and reorganizes it in
# a structure useful for the project.

from mysql.connector import connection
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

con = connection.MySQLConnection(user = 'root', password = 'Boots are awesome.',host = '127.0.0.1', database = 'test_database1',charset = 'utf8', use_unicode = True)
cur = con.cursor()
data = ("SELECT * FROM hello_world")

cur.execute(data)
actual_data = cur.fetchall()

df = pd.DataFrame( [[ij for ij in i] for i in actual_data] )
# df.rename(columns={0:'Rx_Num',1:'X',2:'Y',3:'Z',4:'Distance',5:'Power',6:'Phase'})


# print(df.iloc[:,0].values) # prints indexes
# print(df.iloc[:,:].values) # prints whole table

# Come up with the location size: min and max X and Y coordinates
min_x = min(df.iloc[:,1].values)
min_y = min(df.iloc[:,2].values)
max_x = max(df.iloc[:,1].values)
max_y = max(df.iloc[:,2].values)
print(min_x)
print(min_y)
print(max_x)
print(max_y)


# # Come back later and trying to reorganize it all
# # How do I plot this data? I need X, Y, and Power. 
# X, Y = np.meshgrid(np.array(df.iloc[:,1].values),np.array(df.iloc[:,2].values))
# P_r = np.array(df.iloc[:,5].values)
# print(P_r)
# plt.figure(1)
# plt.plot(X, Y, P_r)