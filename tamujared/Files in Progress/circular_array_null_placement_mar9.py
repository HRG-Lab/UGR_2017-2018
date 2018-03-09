from numpy import sin, cos, exp, pi, arange, log10, deg2rad, max, zeros, array, concatenate, newaxis, min, arccos,\
    rad2deg
from numpy.linalg import inv
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
import numpy as np



def snoi_gen(N, d, scan_ang):

    """ This is a function which is intended to calculate null locations for a uniformly spaced linear array """

    scan_ang = deg2rad(scan_ang)

    cos_scan = cos(scan_ang)
    nulls = []

    if -d*(1+cos_scan) < -1 or d*(1-cos_scan) > 1:
        raise snoi_gen('Scan angle cannot be realized')

    else:
        i = 0

        for n in range(-N+1, N):
            if (n/N) >= -d*(1+cos_scan) and (n/N) <=  d*(1-cos_scan) and n != 0:
                nulls.append(arccos(n/(N*d)+cos_scan))
                i += 1

    nulls = rad2deg(nulls)

    return nulls


# Based Upon Matlab File: linear_DBFreceiver_nullplacer.m by Juan A. Torres-Rosario

# Number of Antennas
N = 5

# radius of array factor
d = 0.5

# Signal of interest location (degrees)
soi = 20

# Generation of Antenna Array Vector
n = arange(0, N, 1)

# Calculation of Weight Coefficients based on Null Placement parameters
Bd = theta_d = array(zeros(N))
Bd[0] = 1
Bd[0] = array([1])
MRA = array([0])
Nulls = array(zeros(N-1))
Nulls_0 = snoi_gen(N, d, soi)
Nulls[0:len(Nulls_0)] = Nulls_0

if len(Nulls) != len(Nulls_0):
    for i in range(0, len(Nulls) - len(Nulls_0)):
        Nulls[len(Nulls_0) + i] = Nulls_0[i] - 0.00001

phi_d = deg2rad(concatenate((MRA, Nulls)))  # Create this

theta_el = 70  # Choose elevation angle to calculate
theta_el = deg2rad(theta_el)
phi_el = 2*pi/N  # Placement of array elements

v_psi_d = array(zeros((len(phi_d), len(phi_d)), dtype=complex))

for k in range(0, len(theta_d)):
    psi_d = 2*pi*d*(cos(phi_el*n)*sin(theta_el)*cos(phi_d[k]) + sin(phi_el*n)*sin(theta_el)*sin(phi_d[k]))
    v = exp(1j * psi_d)
    v_psi_d[:, k] = v

v_psi_d_real = v_psi_d.real
v_psi_d_imag = v_psi_d.imag
w = inv(v_psi_d).T @ Bd.T

# Parameters prior sampling of the Beampattern
sample = 400
phi = arange(0, 360, (360/sample))
theta = arange(0, 180, (180/sample))
phi = deg2rad(phi)
theta = deg2rad(theta)

# Calculation of the Beampattern
BSA_max = 0

v_psi = zeros((len(v_psi_d), len(phi), len(theta)), dtype=complex)
v_psi = array(v_psi)
B = zeros((len(phi), len(theta)), dtype=complex)

for l in range(0, len(theta)):
    for k in range(0, len(phi)):

        v_psi[:, k, l] = exp(2*pi*d*(cos(phi_el*n)*sin(theta[l])*cos(phi[k])
                                     + sin(phi_el*n)*sin(theta[l])*sin(phi[k])))  # Calculate the Array Manifold

        B[k, l] = w.T @ v_psi[:, k, l]  # Calculate the Array Factor

        if abs(B[k, l]) > BSA_max:
            BSA_max = abs(B[k, l])


B = B / max(abs(B))
B_max = max(abs(B))
Bl_max = 20 * log10(B_max)
B_min = min(abs(B))
Bl_min = 20 * log10(B_min)


bx = abs(B)*sin(theta)*cos(phi)  # convert to cartesian coordinates
by = abs(B)*sin(theta)*sin(phi)
bz = abs(B)*cos(theta)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plot = ax.plot_surface(
    bx, by, bz, rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
    linewidth=0, antialiased=False, alpha=0.5)

plt.ylabel('Y')
plt.xlabel('X')
plt.title('Plot')
plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(bx, by, bz, color='b')
# plt.ylabel('Y')
# plt.xlabel('X')
# plt.title('Plot')
# plt.show()



# # Format Plot (Linear)
# fig = plt.figure()
# ax = fig.add_subplot(211)
# plt.grid(True)
# plt.ylabel('AF Magnitude')
# ax.tick_params(which='both', direction='out')
# ax.grid(which='minor', alpha=0.2)
# ax.grid(which='major', alpha=0.5)
# ax.set_xscale('linear')
# ax.set_xticks(array([0, 40, 80, 120, 160, 200, 240, 280, 320, 360]))
# ax.set_yticks(array([-80, -60, -40, -20, 0]))
# ax.set_xlim(0, 180)
# ax.set_ylim(-80, Bl_max+4)
# plt.plot(rad2deg(phi), 20*log10(abs(B)), linewidth=1.3)  # Plot of AF^2 in decibels
#
#
# # Format Plot (Polar)
# ax = plt.subplot(212, polar=True)
# plt.polar(phi, 20*log10(abs(B)), linewidth=1.0)
# ax.set_ylim(-30, 10)
# ax.set_yticks(array([-30, -20, -10, 0]))
# ax.set_xticks(array(deg2rad([-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150])))
#
# plt.show()
