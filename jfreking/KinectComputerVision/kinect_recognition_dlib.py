#import the necessary modules
import glob
import dlib
from skimage import io
from skimage.draw import polygon_perimeter
import sys
import os
#from time import sleep
import timeit
import freenect
import cv2
import numpy as np
import operator
import calibkinect
import serial
import time
 
time.sleep(1)
WIDTH  = 0.252 # m
HEIGHT = 0.252 # m
#detector = dlib.simple_object_detector("/home/jfreking/dlib/detector.svm")

BAUD = 115200
#arduino = serial.Serial('/dev/ttyACM0', BAUD, timeout=0.1)

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    #array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    depth,_ = freenect.sync_get_depth()
    array = depth.astype(np.uint8) #must be an uint8 to display, but must be raw to find position
    return array, depth
    
def initialSetup():
    #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    detector = dlib.simple_object_detector("/home/jfreking/dlib/detector.svm")
    start_time = timeit.default_timer()
    return detector
    
 
if __name__ == "__main__":
    
    #mdev = freenect.open_device(freenect.init(), 0)
    #freenect.set_depth_mode(mdev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_REGISTERED)
    #freenect.runloop(dev=mdev)
    
    detector = initialSetup()
    
    win_rgb = dlib.image_window()
    win_depth = dlib.image_window()
    win_det = dlib.image_window()
    win_det.set_image(detector)
    
    while True:
        #sleep(0.01)
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth, depth1 = get_depth()
        
        if frame is None:
            raise SystemError('Issue grabbing the frame')
            
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
        depth = cv2.resize(depth, (640, 480), interpolation=cv2.INTER_CUBIC)
        
                    
        #numpy_frame = np.asarray(frame)
        #numpy_frame = cv2.normalize(numpy_frame.astype('float'), None, -0.5, 0.5, cv2.NORM_MINMAX)
        #numpy_final = np.expand_dims(numpy_frame, axis=0)
        
        dets = detector(frame)
                        
        #print("Number of objects detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            #    k, d.left(), d.top(), d.right(), d.bottom()))
            
            u,v = np.mgrid[d.left():d.right(), d.top():d.bottom()]
            print("Height/y-pixel: {}".format(HEIGHT/(d.bottom()-d.top())))
            print("Width/x-pixel:  {}".format(WIDTH /(d.right()-d.left())))
            print(" ")
                        
            xyz, uv = calibkinect.depth2xyzuv(depth1[v,u], u, v)
                                    
            if len(xyz) != 0:
                
                #print(depth_dets[k-1].bottom()) #+= 20
                #depth_dets[k-1].set_bottom(depth_dets[k-1].bottom()+20)
                #print(depth_dets[k-1].bottom())
                
                #x_ind = np.argmin(abs(xyz[:,0]))
                #y_ind = len(xyz[:,1])/2 #np.argmin(abs(xyz[:,1]))            
                z_ind = len(xyz[:,2])/2#np.argmin(abs(xyz[:,2]))
                
                x = np.median(xyz[:,0]) #xyz[x_ind,0] #+ 0.03 
                y = np.average(xyz[:,1]) #xyz[y_ind,1] #+ 0.04
                z = np.median(xyz[:,2]) #xyz[z_ind,2] #- 0.04
                
                print("x [m]: {}".format(x))
                print("y [m]: {}".format(y))            
                print("z [m]: {}".format(z))
                print(" ")
                print("uv: {}".format(uv))
                print(" ")
                p = np.sqrt(x**2 + y**2 + z**2)
                theta = np.arccos(y/p)
                phi = np.arctan(-z/x)
                
                #print("p [m]: {}".format(p))
                #print("theta [rad]: {}".format(theta))
                #print("phi [rad]: {}".format(phi))
                #print(" ")
                
                #arduino.write(z.astype('float'))
                #data = arduino.readline()
                
                #if data:
                #    print data.rstrip('\n')
            
        
        win_rgb.clear_overlay()
        win_rgb.set_image(frame)
        win_rgb.add_overlay(dets)
        
        win_depth.clear_overlay()
        win_depth.set_image(depth)
        win_depth.add_overlay(dets)
        
        #classify(numpy_final)
        #predictions = sess.run(softmax_tensor, {'Mul:0': numpy_final})
            
                     
        #sort to show labels of first prediction in order of confidence
        #top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        """    
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
        """       
        


        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break


    #cv2.destroyAllWindows()
    
