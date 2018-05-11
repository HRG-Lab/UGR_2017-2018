# Digital Beamforming Experiment #


### Description of Current Project ###

We are performing an experiment in which we set up multiple antenna arrays in some space which will track a moving object while in the presence of a jammer.

<!-- ###### 2D Render of the Final Project -->

<!-- <img src="https://user-images.githubusercontent.com/29260218/36869534-bde85992-1d61-11e8-848a-c8eaaedd3720.JPG" width="450"> -->

- - - -

## Progress ##


* March 2
    * Progress:
        * Created a linear array python script (linear_array_null_placement_animated.py) in which we can steer a beam and place nulls in arbitrary locations <br />
        <img src="https://user-images.githubusercontent.com/29260218/37219953-ac570a64-238a-11e8-99b1-2b654939b2c7.png" width="250"> <br />
        *Pictured Above: 48 element linear array with half wavelength spacing directed at 70 degrees, nulled at  45 degrees* <br /> <br />
    * Goal For Next Week:
        * Create a circular array python script in which we can steer a beam and place nulls in arbitrary locations
    
 - - - -
* March 9
    * Progress:
        * Researched more heavily into the math behind Juan A. Torres-Rosario's antenna array research paper
            - Paper Source: <https://arrc.ou.edu/~rockee/RIO/torresrosario.pdf>
        * Created a 3D Circular Array Python script (circular_array_null_placement_mar9.py) which severely needs debugging <br />
        <img src="https://user-images.githubusercontent.com/29260218/37219169-3ff91e7c-2388-11e8-8771-8444e2171b77.png" width="250"> <br />
        *Pictured Above: Output of Current Script* <br /> <br />
    * Goal For Next Week:
        * Debug the circular array script into something that works
_ _ _ _
* March 16
    * Progress:
        * 3d circular array script now accurately plots a circular planar array (circular_array_null_placement.py) <br />
<img src="https://user-images.githubusercontent.com/29260218/37626992-613a10bc-2ba0-11e8-869f-d1df10cc3c98.png" width="250"> <br />
        *Pictured Above: 8 element circular array with a radius of 1 wavelength, weights are uniform* <br /> <br />
    * Goal For This weekend:
        * Create an array weighting algorithm based upon the Schelkunoff method or by performing a Fourier transform
_ _ _ _
* March 19
    * Progress:
        * Found a paper that attempts to do a similar task. They use an LMS method to calculate their weighting functions.
            - Paper Source: <http://ieeexplore.ieee.org/document/5494450/>
    * Goal:
        * Finish creating the weighting function using the above source
____
* March 23
    - Progress:
        + Found more articles about the weighting method used (Frost LMS Algorithm) and created a weighting algorithm which needs to be debugged.
            * Van Trees Book: <https://library.tamu.edu> (Type in "Van Trees Array")
            * Matlab Code help with the given examples and some problems: <https://www.mathworks.com/matlabcentral/fileexchange/46514-optimum-array-processing--van-trees--solutions-and-figures>
            * Tutorial on how to implement (Cited in Van Trees): <http://ieeexplore.ieee.org/document/774932/>
    - Goal for this week:
        *   Need to ask for help/review more on the Frost Algorithm to get it to properly implemented.
____
* March 30: Assigned to look over and familiarize ourselves with HFSS
    - Progress:
        + Completed multiple tutorials on modelling dipole antennas and the provided tutorial on modelling patch antennas
___

* April 3: Links to possibly helpful resources
    - Dr. Huff sent us this link over DOA techniques:
        + <http://www.faculty.jacobs-university.de/jwallace/xwallace/courses/ap/ch5c.pdf>
    - MIT Course: Adaptive Antennas and Phased Arrays (look at first couple of lectures for adaptive nulling):
        + <https://www.ll.mit.edu//workshops/education/videocourses/antennas/index.html>
    - Mit Course: Recievers, Antennas and Signals:
        + <https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-661-receivers-antennas-and-signals-spring-2003/>

    - I'm coming to the realization I'm gonna need a deeper understanding of Signal Proceessing
        + MIT Course: Introduction to Communication, Control, and Signal Processing
            * <https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-011-introduction-to-communication-control-and-signal-processing-spring-2010/>
        + MIT Course: Digital Signal Processing
            * <https://ocw.mit.edu/resources/res-6-008-digital-signal-processing-spring-2011/>
____

* April 8:
    - Progress: Set up Josh's HFSS Python Scripts on the HRG lab computers allowing us to manipulate the weights of the antenna beams significantly easier than having to individually punch each individual weight.
    - Have begun watching some Adaptive Signal Processing Tutorials in order to catch us up to speed on the techniques needed to implement the weighting algorthm.
        + Intro to Adaptive Filters: <https://www.youtube.com/watch?v=ya0-S1apej8> (Around minute 19, he talks about Antenna Arrays as a simple example)
    - Great Link for Adaptive Signal Processing 
        + <http://www.cs.tut.fi/~tabus/course/ASP/Lectures_ASP.html>
____

* April 13:
    - Looked over the Adaptive Signal Processing Link
    - Was able to verify my linear array script in HFSS, see the signal nulling repository for the code I am using below link: <https://github.com/HRG-Lab/Null_Placement>
        + This code requires this submodule: <https://github.com/HRG-Lab/HFSS_Python/wiki/Including-HFSS_Python>
____ 
* April 19:
    - Introduction to Space-Time Wireless Communication: <https://www.scribd.com/document/261312438/Arogyaswami-Paulraj-Rohit-Nabar-Dhananjay-Gore-Introduction-to-Space-time-Wireless-Communications>

___ 
* April 27:
    - <https://www.youtube.com/watch?v=hc2Zj55j1zU&t=1684s> LMS taught by Widrow
    - <https://en.wikipedia.org/wiki/Least_mean_squares_filter> LMS Wikipedia

___
* May 7
    - <http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=EB4CCA9B6E66B0BCA383CC923B5A3ECC?doi=10.1.1.105.434&rep=rep1&type=pdf>
    - <http://www.site.uottawa.ca/~sloyka/elg5132/Lec_1_ELG5132.pdf>
    <br />
    - Began script for beamforming using LMS for linear array
___
* May 10:
    - Never added the simulation results to the readme
    - All tests were done with HFSS in conjuction with a Python script
    - The picture on the right is the Python Script, picture on the left are the simulated results
    
    <br />
    <img src="https://user-images.githubusercontent.com/29260218/39897858-cb0b3636-5479-11e8-9cce-fc53156e3878.png" width="500"> <br />
    *Picture of the setup used, 3 antennas with half wavelength spacing* <br /> <br /> <br />

    <img src="https://user-images.githubusercontent.com/29260218/39897694-08cf5bf6-5479-11e8-860f-9c09ade974dc.png" width="500"> <br />
    *SOI placed at 20 degrees, null placed at 10 degrees* <br /> <br /> <br />

    <img src="https://user-images.githubusercontent.com/29260218/39897820-a2a7c0a6-5479-11e8-9896-d9b1f1a0fefc.png" width="500"> <br />
    *SOI placed at 20 degrees, null placed at 10 degrees* <br /> <br /> <br />




