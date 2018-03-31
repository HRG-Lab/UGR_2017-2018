# Digital Beamforming Experiment #


### Description of Current Project ###

We are performing an experiment in which we set up multiple antenna arrays in some space which will track an object a moving object while in the presence of a jammer.

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

* March 23
    - Progress:
        + Found more articles about the weighting method used (Frost LMS Algorithm) and created a weighting algorithm which needs to be debugged.
            * Van Trees Book: <https://library.tamu.edu> (Type in "Van Trees Array")
            * Matlab Code help with the given examples and some problems: <https://www.mathworks.com/matlabcentral/fileexchange/46514-optimum-array-processing--van-trees--solutions-and-figures>
            * Tutorial on how to implement (Cited in Van Trees): <http://ieeexplore.ieee.org/document/774932/>
    - Goal for this week:
        *   Need to ask for help/review more on the Frost Algorithm to get it to properly implemented.
* March 30: Assigned to look over and familiarize ourselves with HFSS
    - Progress:
        + Completed multiple tutorials on modelling dipole antennas and the provided tutorial on modelling patch antennas
___
