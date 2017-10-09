#import the necessary modules
import tensorflow as tf
import sys
import os
import timeit
import freenect
import cv2
import numpy as np
 
#Load label file, strip off carriage return
label_lines =[line.rstrip() for line in tf.gfile.GFile("/home/jfreking/tensorflow-retrain/tf_files/retrained_labels.txt")]
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array
    
def initialSetup():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    start_time = timeit.default_timer()
    
    #Unpersists graph from file
    with tf.gfile.FastGFile("/home/jfreking/tensorflow-retrain/tf_files/retrained_graph.pb",'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='') 
        
    #print("Took {} seconds to unpersist the graph".format(timeit.default_timer()-start_time))

 
if __name__ == "__main__":
    initialSetup()

    with tf.Session() as sess:
            start_time = timeit.default_timer()
            #Feed image_data ass input to graph for first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            
            while True:
                #get a frame from RGB camera
                frame = get_video()
                #get a frame from depth sensor
                depth = get_depth()
        
                if frame is None:
                    raise SystemError('Issue grabbing the frame')
            
                frame = cv2.resize(frame, (299, 299), interpolation=cv2.INTER_CUBIC)
                depth = cv2.resize(depth, (299, 299), interpolation=cv2.INTER_CUBIC)
                #display RGB image
                cv2.imshow('RGB image',frame)
                #display depth image
                cv2.imshow('Depth image',depth)
                    
                numpy_frame = np.asarray(frame)
                numpy_frame = cv2.normalize(numpy_frame.astype('float'), None, -0.5, 0.5, cv2.NORM_MINMAX)
                numpy_final = np.expand_dims(numpy_frame, axis=0)

                #classify(numpy_final)
                predictions = sess.run(softmax_tensor, {'Mul:0': numpy_final})
            
                     
                #sort to show labels of first prediction in order of confidence
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            
                for node_id in top_k:
                    human_string = label_lines[node_id]
                    score = predictions[0][node_id]
                    print('%s (score = %.5f)' % (human_string, score))
                
                print(" ")
                print(" ")


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                #print("Tensor")
                #print("Took {} seconds".format(timeit.default_timer()-start_time))

    cv2.destroyAllWindows()
