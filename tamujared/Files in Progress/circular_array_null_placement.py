from numpy import sin, cos, exp, pi, arange, log10, deg2rad, max, zeros, array, concatenate, newaxis, min, arccos,\
    rad2deg
from numpy.linalg import inv
import matplotlib.pyplot as plt


""" The current goal is modify this script into a circular array script """

def snoi_gen(N, d, scan_ang):

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






# # Based Upon matlab File: linear_DBFreceiver_nullplacer.m

# Number of Antennas
N = 5

# Spacing in wavelengths
d = 0.5

# Signal of interest location (degrees)
soi = 20
null = 80

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
# Nulls[len(Nulls) - 1] = snoi

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

    SA = SA + d * abs(B[k])**2 * sin(theta[k] * pi / 180) * (180 / sample) * (pi / 180)

    if abs(B[k]) > BSA_max:
        BSA_max = abs(B[k])


B = B / max(abs(B))
B_max = max(abs(B))
Bl_max = 20 * log10(B_max)
B_min = min(abs(B))
Bl_min = 20 * log10(B_min)


# Format Plot (Linear)
fig = plt.figure()
ax = fig.add_subplot(211)
plt.grid(True)
plt.ylabel('AF Magnitude')
ax.tick_params(which='both', direction='out')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)
ax.set_xscale('linear')
ax.set_xticks(array([0, 40, 80, 120, 160, 200, 240, 280, 320, 360]))
ax.set_yticks(array([-80, -60, -40, -20, 0]))
ax.set_xlim(0, 180)
ax.set_ylim(-80, Bl_max+4)
plt.plot(theta, 20*log10(abs(B)), linewidth=1.3)


# Format Plot (Polar)
ax = plt.subplot(212, polar=True)
plt.polar(deg2rad(theta), 20*log10(abs(B)), linewidth=1.0)
ax.set_ylim(-30, 10)
ax.set_yticks(array([-30, -20, -10, 0]))
ax.set_xticks(array(deg2rad([-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150])))

plt.show()
