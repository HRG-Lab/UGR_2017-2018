import numpy as np
import cv2
from socket import *
import socket
import os
import sys
import netifaces as ni

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

codeword = '12'

# Uncomment to tune tracker to a different color
"""
def nothing(x):
    pass
    
cv2.namedWindow('HSV Tuner')

cv2.createTrackbar('Hmin', 'HSV Tuner', 0, 180, nothing)
cv2.createTrackbar('Hmax', 'HSV Tuner', 0, 180, nothing)
cv2.createTrackbar('Smin', 'HSV Tuner', 0, 255, nothing)
cv2.createTrackbar('Smax', 'HSV Tuner', 0, 255, nothing)
cv2.createTrackbar('Vmin', 'HSV Tuner', 0, 255, nothing)
cv2.createTrackbar('Vmax', 'HSV Tuner', 0, 255, nothing)

"""
while True:
    # Uncomment to tune tracker to a different color
    """
    # Get slider positions
    hMin = cv2.getTrackbarPos('Hmin', 'HSV Tuner')
    hMax = cv2.getTrackbarPos('Hmax', 'HSV Tuner')
    sMin = cv2.getTrackbarPos('Smin', 'HSV Tuner')
    sMax = cv2.getTrackbarPos('Smax', 'HSV Tuner')
    vMin = cv2.getTrackbarPos('Vmin', 'HSV Tuner')
    vMax = cv2.getTrackbarPos('Vmax', 'HSV Tuner')
    """
    
    # Set HSV thresholds
    # Uncomment to tune tracker to a different color
    lw_range = np.array([117,55,147]) #np.array([hMin,sMin,vMin])
    up_range = np.array([180,114,234]) #np.array([hMax,sMax,vMax])
    
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
        if (X <= 80):
            codeword = '00'
        elif (X > 80 and X <= 160):
            codeword = '01'
        elif (X > 160 and X <= 240):
            codeword = '02'
        elif (X > 240 and X <= 320):
            codeword = '03'
        elif (X > 320 and X <= 400):
            codeword = '04'
        elif (X > 400 and X <= 480):
            codeword = '05'
        elif (X > 480 and X <= 560):
            codeword = '06'
        elif (X > 560 and X <= 640):
            codeword = '07'
        elif (X > 640 and X <= 720):
            codewrod = '08'
        elif (X > 720 and X <= 800):
            codeword = '09'
        elif (X > 800 and X <= 880):
            codeword = '10'
        elif (X > 880 and X <= 960):
            codeword = '11'
        elif (X > 960 and X <= 1040):
            codeword = '12'
        elif (X > 1040 and X <= 1120):
            codeword = '13'
        elif (X > 1120 and X <= 1200):
            codeword = '14'
        elif (X > 1200 and X <= 1280):
            codeword = '15'
        elif (X > 1280 and X <= 1360):
            codeword = '16'
        elif (X > 1360 and X <= 1440):
            codeword = '17'
        elif (X > 1440 and X <= 1520):
            codeword = '18'
        elif (X > 1520 and X <= 1600):
            codeword = '19'
        elif (X > 1600 and X <= 1680):
            codeword = '20'
        elif (X > 1680 and X <= 1760):
            codeword = '21'
        elif (X > 1760 and X <= 1840):
            codeword = '22'
        elif (X > 1840 and X <= 1920):
            codeword = '23'
        else:
            codeword = '11'
        
        """
        if (X < 320 and Y < 270):
            codeword = '01'
        elif (X < 320 and (Y >= 270 and Y < 540)):
            codeword = '02'
        elif X < 320 and (Y >=5400 and Y < 810):
            codeword = '03'
        elif X < 320 and Y >= 810:
            codeword = '04'
        elif (X >= 320 and X < 640) and Y < 270:
            codeword = '05'
        elif (X >= 320 and X < 640) and (Y >= 270 and Y < 540):
            codeword = '06'
        elif (X >= 320 and X < 640) and (Y >= 540 and Y < 810):
            codeword = '07'
        elif (X >= 320 and X < 640) and Y >= 810:
            codeword = '08'
        elif (X >= 640 and X < 960) and Y < 270:
            codeword = '09'
        elif (X >= 640 and X < 960) and (Y >= 270 and Y < 540):
            codeword = '10'
        elif (X >= 640 and X < 960) and (Y >= 540 and Y < 810):
            codeword = '11'
        elif (X >= 640 and X < 960) and Y >= 810:
            codeword = '12'
        elif (X >= 960 and X < 1280) and Y < 270:
            codeword = '13'
        elif (X >= 960 and X < 1280) and (Y >= 270 and Y < 540):
            codeword = '14'
        elif (X >= 960 and X < 1280) and (Y >= 540 and Y < 810):
            codeword = '15'
        elif (X >= 960 and X < 1280) and Y >= 810:
            codeword = '16'
        elif (X >= 1280 and X < 1600) and Y < 270:
            codeword = '17'
        elif (X >= 1280 and X < 1600) and (Y >= 270 and Y < 540):
            codeword = '18'
        elif (X >= 1280 and X < 1600) and (Y >= 540 and Y < 810):
            codeword = '19'
        elif (X >= 1280 and X < 1600) and Y >= 810:
            codeword = '20'
        elif X >= 1600 and Y < 270:
            codeword = '21'
        elif X >= 1600 and (Y >= 270 and Y < 540):
            codeword = '22'
        elif X >= 1600 and (Y >= 540 and Y < 810):
            codeword = '23'
        elif X >= 1600 and Y >= 810:
            codeword = '24'
        else:
            codeword = '12'
        """
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
