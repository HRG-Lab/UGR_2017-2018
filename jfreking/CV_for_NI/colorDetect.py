import numpy as np
import cv2
from socket import *
import socket
import os
import sys
import pandas as pd
import netifaces as ni

# Get codewords from Excel file
codebook = pd.read_excel('/home/jfreking/Desktop/1920_codewords_azimuth_only.xlsx',header=0)

txCodes = codebook['TX Codewords']
#print txCodes

# Get IP address (check the available links with cmd: ifconfig -- connection may be 'eth0')
ni.ifaddresses('enp3s0')
ip = ni.ifaddresses('enp3s0')[ni.AF_INET][0]['addr']
print ip


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_address = (ip, 8085) #server name, port number
print >>sys.stderr, 'starting up on %s port %s' % server_address
try:
    sock.bind(server_address)
except socket.error as msg:
    print 'Bind failed.Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
    sys.exit()
    
print 'Socket bind complete'

# If no connection is available in 2 seconds of trying to send data, raise error
sock.setblocking(1)
sock.settimeout(0.1)

# Listen for incoming connections -- accept waits for an incoming connection
sock.listen(10)
print 'Socket listening'  

cap = cv2.VideoCapture(1)

#codeword = '12'

# Uncomment to tune tracker to a different color

def nothing(x):
    pass
    
cv2.namedWindow('HSV Tuner')

cv2.createTrackbar('Hmin', 'HSV Tuner', 0, 180, nothing)
cv2.createTrackbar('Hmax', 'HSV Tuner', 0, 180, nothing)
cv2.createTrackbar('Smin', 'HSV Tuner', 0, 255, nothing)
cv2.createTrackbar('Smax', 'HSV Tuner', 0, 255, nothing)
cv2.createTrackbar('Vmin', 'HSV Tuner', 0, 255, nothing)
cv2.createTrackbar('Vmax', 'HSV Tuner', 0, 255, nothing)


while True:
    # Uncomment to tune tracker to a different color
    
    # Get slider positions
    hMin = cv2.getTrackbarPos('Hmin', 'HSV Tuner')
    hMax = cv2.getTrackbarPos('Hmax', 'HSV Tuner')
    sMin = cv2.getTrackbarPos('Smin', 'HSV Tuner')
    sMax = cv2.getTrackbarPos('Smax', 'HSV Tuner')
    vMin = cv2.getTrackbarPos('Vmin', 'HSV Tuner')
    vMax = cv2.getTrackbarPos('Vmax', 'HSV Tuner')
    
    
    # Set HSV thresholds
    # Uncomment to tune tracker to a different color
    lw_range = np.array([hMin,sMin,vMin])
    up_range = np.array([hMax,sMax,vMax])
    
    # Get frame from camera
    ret, frame = cap.read()
    
    # Logitech C920 has a resolution of 1920x1080
    frame = cv2.resize(frame, (1920,1080))
        
    # Convert frame to HSV
    hsv_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    # Define frame threshold with HSV thresholds
    frame_threshold = cv2.inRange(hsv_img, lw_range, up_range)
    
    # Find contours
    ret,thresh = cv2.threshold(frame_threshold, 127, 255, 0)
    _, contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find center of largest contour and produce a codeword based on position
    #   Note: codeword MUST be a string for TCP/IP communication
    if contours != []:
        areas = [cv2.contourArea(c) for c in contours]
        maxIndex = np.argmax(areas)
        cnt = contours[maxIndex]

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        
        cv2.rectangle(frame_threshold, (x,y), (x+w, y+h), (180,255,255), 2)
        
        X = x+w/2
        Y = y+h/2
        
        #resolution: 1920x1080
        codeword = str(txCodes[X])
        
        
        #DEGBUGGING
        """
        print("x: {}".format(X))
        print("y: {}".format(Y))
        print(" ")            
        print 'codeword: ' + codeword
        print(" ")
        """
    
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    # Try to accept a client
    try:
        conn, client_address = sock.accept() #returns open connection btwn server and client and the client address
        
        # Send codeword if there is a connection, if no connection, print error and continue
        try:
            conn.sendall(codeword)
        except socket.error as msg:
            print 'No connection available. Error Code: ' + str(msg[0]) + ' Error Msg: ', msg[1]
            continue
        
    except timeout:
        print 'caught a timeout'
    
    
    
    cv2.imshow("Show", frame)
    cv2.imshow("HSV", frame_threshold)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

conn.close()
cap.release()
cv2.destroyAllWindows()
