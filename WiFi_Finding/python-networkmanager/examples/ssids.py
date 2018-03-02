"""
Display all visible SSIDs
"""

import NetworkManager
import csv
import numpy as np

def write_csv(data):
    with open('/home/jfreking/pythonProject/wifi_216.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

i = 0

while i <= 200:
    i = i + 1
    if np.mod(i,5) == 0:
        for dev in NetworkManager.NetworkManager.GetDevices():
            if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
                continue
            for ap in dev.GetAccessPoints():
                print('%-30s %dMHz %d%%' % (ap.Ssid, ap.Frequency, ap.Strength))
                data = [ap.HwAddress, ap.Strength]
                write_csv(data)
                
                
                
