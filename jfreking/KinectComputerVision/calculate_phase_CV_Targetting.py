# calculate the phases of the volumetric Random Array according to
# the scan angles

import numpy as np


numElements = 16
rad=np.pi/180
f=2.46e9
lumda = (3e8)/f

def calcPhase(x, y, z, Position=np.zeros((numElements,3))):

    # Original Positions (global coordinates)
    Position=[
        [-120, -220, 85],
        [-170, -180, 56],
        [42, 10, 260],
        [260, -198, -3],
        [89, -222, 60],
        [89, 54, 154],
        [-240, 36, -200],
        [-146, 219, 180],
        [-209, 93, 90],
        [206, -29, -260],
        [46, 203, -168],
        [180, 19, -280],
        [70, 32, -222],
        [12, 108, 239],
        [-218, -80, -189],
        [-242, -157, -178],
        #[244, 99, -217],
        #[-240, 220, 59],
        #[-60, -56, 260],
        #[-160, 160, 263],
        #[35, -156, 189],
        #[-298, -120, -11],
        #[160, -60, 91],
        #[209, 200, -68],
        #[250, 67, 217],
        #[73, -66, 92],
        #[3, 84, -39],
        #[-138, -216, -183],
        #[160, -144, -250],
        #[4, -230, -245],
        #[-48, -43, -42],
        #[160, -146, 276]
    ]


    T=[[x],[y],[z]]

    O=np.dot(Position,T)

    phases = np.zeros((numElements,1))
    for i in range(numElements):

       if (O[i]<=0):
          phases[i] = (abs(O[i])*(10**-3)*360/lumda) * -1
        
       elif (O[i]>0):
          phases[i] = (abs(O[i])*(10**-3)*360/lumda)
       
       if (abs(phases[i]) >= 360):
          phases[i] = np.mod(phases[i],360)



    # transfer to HFSS values
    # our phase delay should *-1 = HFSS
    phases = phases*-1
    
    # want phase shifters to run in +90 - +450 degree range (1.22V and up)
    # when using HMC928LP5E
    phases = phases + 90
    
    #print phases
    return phases
    


