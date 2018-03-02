#from kivy.uix.screenmanager import ScreenManager, Screen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import NetworkManager
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

"""
from kivy.app import App
from kivy.lang import Builder


# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string(
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
            )

# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
"""

#Bring in data from csv
room219 = pd.read_csv(open('/home/jfreking/pythonProject/wifi_data_219.csv'), delimiter=',',header=None)
room206 = pd.read_csv(open('/home/jfreking/pythonProject/wifi_data_206.csv'), delimiter=',',header=None)

#Make them arrays
room219 = np.array(room219)
room206 = np.array(room206)

#Put them together
dataSet = np.append(room219, room206, 0)
#print dataSet

#Assign unique identifiers for each MAC address to make the data easier to model
unique = []
for i in range(len(dataSet[:,0])):
    if i == 0:
        unique.append(dataSet[i,0])
        dataSet[i,0] = 0
    else:# len(unique) < len(uniq_):
        dataSetTemp = dataSet[i,0]
        for j in range(len(unique)):
            if dataSetTemp == unique[j]:
                dataSetTemp = j
            elif j == len(unique) - 1 and dataSet[i,0] == dataSetTemp:
                unique.append(dataSet[i,0])
                dataSetTemp = j+1
        dataSet[i,0] = dataSetTemp        
            
#print dataSet
#print unique

#Assign features and solutions (solutions only necessary for supervised learning)
X = dataSet #np.append(room219, room206, 0)
#y = np.append(219*np.ones(len(room219[:,0])), 206*np.ones(len(room206[:,0])),0)

#X_train, X_test, y_train, y_test = \
#        train_test_split(X, y, test_size=.4, random_state=42)
#print 'Y = ', y
#print 'X = ', X


#X = StandardScaler().fit_transform(X)

"""
for name, est in estimators:
    est.fit(X_train)
    labels = est.labels_
    prediction = est.predict(X_test)
    
    plt.scatter(X[0:len(room219)-1,0],X[0:len(room219)-1,1])
    plt.scatter(X[len(room219):len(room219)+len(room206[:,0]),0],X[len(room219):len(room219)+len(room206[:,0]),1],color='r')
    plt.scatter(est.cluster_centers_[:,0],est.cluster_centers_[:,1], color='y',linewidths=10)
    plt.show()
 """ 
#Apply K Means algorithm, 2 clusters for 2 rooms    
KMeans = KMeans(n_clusters=2, random_state=0)

KMeans.fit(X)
labels = KMeans.labels_

plt.scatter(X[0:len(room219)-1,0],X[0:len(room219)-1,1])
plt.scatter(X[len(room219):len(room219)+len(room206[:,0]),0],X[len(room219):len(room219)+len(room206[:,0]),1],color='r')
plt.scatter(KMeans.cluster_centers_[:,0],KMeans.cluster_centers_[:,1], color='y',linewidths=10)
plt.show()



k = 0
"""
state = ""
"""
while True:#sm.current_screen == 'SettingsScreen':

    X_test = []
    k += 1
    if np.mod(k,100000) == 0:
        k = 0
        for dev in NetworkManager.NetworkManager.GetDevices():
            if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
                continue
            for ap in dev.GetAccessPoints():
                try:
                    #print('%-30s %s %d%%' % (ap.Ssid, ap.HwAddress, ap.Strength))
                    data = [ap.HwAddress,ap.Strength]
                    #print str(data[0])
                    for j in range(len(unique)):
                        #print data[0]
                        if str(data[0]) == str(unique[j]):
                            #print(str(unique[j]))
                            data[0] = j
                            break
                        elif j == len(unique)-1:
                            data[0] = 0
                            break
                                
                    #print data
                    X_test.append(data)
                    #print X_test

                except NetworkManager.ObjectVanished:
                    pass
                
            
            prediction = KMeans.predict(X_test)
            print stats.mode(prediction)[0][0]
            
            if stats.mode(prediction)[0][0] == 0: #and state != "219":
                print "You are at room 219."
                #state = "219"
            #elif stats.mode(prediction)[0][0] == 0:
             #   print "You are at the corner between room 219 and room 216."
            elif stats.mode(prediction)[0][0] == 1: #and state != "216":
                print "You are at room 216"
                #state = "216"    




