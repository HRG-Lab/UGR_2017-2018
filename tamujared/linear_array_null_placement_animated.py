from numpy import sin, cos, exp, pi, arange, log10, deg2rad, max, zeros, array, concatenate, newaxis, min, arccos, resize, ceil, rad2deg
from numpy.linalg import inv
import matplotlib.pyplot as plt
import numpy as np


def snoi_gen(N, d, scan_ang):

    scan_ang = deg2rad(scan_ang)

    cos_scan = cos(scan_ang)
    nulls = []

    if -d*(1+cos_scan) < -1 or d*(1-cos_scan) > 1:
        raise snoi_gen('Scan angle cannot be realized')

    else:
        i = 0

        for n in range(-N+1, N):
            # print(n)
            # print(str(n/N) + ' >= ' + str(-d*(1+cos_scan)) + ' and ' + str(n/N) + ' <= ' + str(d*(1-cos_scan)))
            if (n/N) >= -d*(1+cos_scan) and (n/N) <=  d*(1-cos_scan) and n != 0:
                # print(n/(N*d)+cos_scan)
                nulls.append(arccos(n/(N*d)+cos_scan))
                i += 1

    nulls = rad2deg(nulls)

    return nulls






# # File: linear_DBFreceiver_nullplacer.m


# Number of Antennas
N = 50

# Spacing in wavelengths
d = 0.5

# Signal of interest location (degrees)
soi = 20
snoi = 45

def createAF(N,d,soi,snoi):
    # Generation of Antenna Array Vector
    n = arange(0, N, 1)

    # Calculation of Weight Coefficients based on Null Placement parameters
    Bd = array(zeros(N))
    Bd[0] = 1
    Bd[0] = array([1])
    MRA = array([0])
    Nulls = array(zeros(N - 1))
    Nulls_0 = snoi_gen(N, d, soi)
    Nulls[0:len(Nulls_0)] = Nulls_0

    if len(Nulls) != len(Nulls_0):
        for i in range(0, len(Nulls) - len(Nulls_0)):
            Nulls[len(Nulls_0)+ i] = Nulls_0[i] - 0.00001
            # Nulls[len(Nulls_0) + i] = input('Input static null:')
    Nulls[len(Nulls)-1] = snoi

    print(Nulls)

    theta_d = concatenate((MRA, Nulls))
    sai_d = pi * cos(theta_d * pi / 180)

    v_sai_d_len = len(theta_d)
    v_sai_d = zeros((v_sai_d_len, v_sai_d_len), dtype=complex)
    v_sai_d = array(v_sai_d)

    for k in range(0, len(theta_d)):
        v = exp(1j * (n - (N - 1) / 2) * sai_d[k])[newaxis]
        v_sai_d[:, k] = v

    w = inv(v_sai_d).T @ Bd.T


    # Parameters prior sampling of the Beampattern
    sample = 1000
    theta = arange(0, 360, (180/sample))  # theta = 0:(180 / sample): 360;
    sai = pi * cos(theta * pi / 180)

    # Calculation of the Beampattern
    SA = 0
    BSA_max = 0

    v_sai = zeros((v_sai_d_len, len(theta)), dtype=complex)
    v_sai = array(v_sai)
    B = zeros(len(theta), dtype=complex)

    for k in range(0, len(theta)):

        v0 = exp(1j * (n - (N - 1) / 2) * sai[k])
        v_sai[:, k] = v0

        B[k] = w.T @ v_sai[:, k]

        SA = SA + 0.5 * abs(B[k])**2 * sin(theta[k] * pi / 180) * (180 / sample) * (pi / 180)

        if abs(B[k]) > BSA_max:
            BSA_max = abs(B[k])

    B = B / max(abs(B))

    AF = 20 * log10(abs(B))

    return AF

sample = 1000
theta = arange(0, 360, (180/sample))

def animate(theta, theta_zero_new, theta_zero_old):
    while theta_zero_old != theta_zero_new:
        if theta_zero_old > theta_zero_new:
            theta_zero_old -= 1
        else:
            theta_zero_old += 1
        plt.clf()
        soi=theta_zero_old
        AF = createAF(N, d, soi, snoi)
        ax = plt.subplot(111, polar=True)
        ax.set_ylim(-30, 10)
        ax.set_yticks(array([-30, -20, -10, 0, 10]))
        ax.set_xticks(array([0, -30, -45, -60, -90, -120, -135, -150, 180, 150, 135, 120, 90, 60, 45, 30]) / 180 * pi)
        plt.plot(deg2rad(theta), AF, linewidth=1.0)
        plt.pause(.0001)



theta_zero_new = soi
loop = True
while(loop):
    theta_zero_old = theta_zero_new
    soi=theta_zero_old
    AF = createAF(N,d,soi, snoi)
    ax = plt.subplot(111, polar=True)
    plt.plot(deg2rad(theta), AF, linewidth=1.0)
    ax.set_ybound(-30, 10)
    ax.set_yticks(array([-30, -20, -10, 0, 10]))
    ax.set_xticks(array([0, -30, -45, -60, -90, -120, -135, -150, 180, 150, 135, 120, 90, 60, 45, 30]) / 180 * pi)
    plt.pause(0.01)
    stage_variable=input('Enter new scan angle, enter "q" to quit: ')
    if stage_variable.isdigit() :
        theta_zero_new = int(stage_variable)
    else:
        loop = False
    animate(theta, theta_zero_new, theta_zero_old)
