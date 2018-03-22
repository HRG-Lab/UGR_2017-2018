from numpy import sin, cos, exp, pi, arange, log10, deg2rad, max, zeros, ones, array, concatenate, newaxis, min, arccos,\
    rad2deg, meshgrid, append, linspace, concatenate
from numpy.linalg import inv
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d


def snoi_gen(N, d, null_num, theta_null, phi_null):  # (N=8, d=1, null_num=2, theta_null=[20, 40], phi_null=[20, 40])
    theta_null, phi_null = deg2rad(theta_null), deg2rad(phi_null)
    n = arange(0, N, 1)
    phi_el = 2 * pi / N

    v_k = array(zeros(N), dtype=complex)
    dv_k = array(zeros(N), dtype=complex)
    dv_k2 = array(zeros((N, N), dtype=complex))
    C_0 = array(zeros((N, null_num), dtype=complex))
    C_1 = array(zeros((N, null_num), dtype=complex))  # am actually unsure of the size
    C_2 = array(zeros((N, null_num), dtype=complex))  # am actually unsure of the size

    for i in range(0, N):
        v_k = exp(1j*2*pi*d*(sin(theta_null[i])*cos((phi_el*n) - phi_null[i])))
        v_k_real = v_k.real  # debug
        dv_k = (1j*2*pi*d)*exp(1j*2*pi*d*(sin(theta_null[i])*cos((phi_el*n) - phi_null[i])))
        dv_k2 = -1*(2*pi*d)**2*exp(1j * 2 * pi * d * (sin(theta_null[i]) * cos((phi_el * n) - phi_null[i])))

        C_0[:, i] = v_k
        C_1[: i] = dv_k
        C_2[:, i] = dv_k2

    C = concatenate(C_0, C_1)
    C = concatenate(C, C_2)



    nulls = 0
    return nulls

def main():
    # Based Upon Matlab File: linear_DBFreceiver_nullplacer.m by Juan A. Torres-Rosario

    # Number of Antennas
    N = 8

    # radius of the circular array factor
    d = 1

    # Signal of interest location (degrees)
    soi = 20

    # Generation of Antenna Array Vector
    n = arange(0, N, 1)




    # Parameters prior sampling of the Beampattern (The other program did it all in a weird way, so I'm doing it a better
    # more intuitive way)
    n = arange(0, N, 1)
    sample = 100
    phi = linspace(0, 360, sample)
    theta = linspace(0, 90, sample)
    phi_el = 2*pi/N  # Placement of array elements

    phi = deg2rad(phi)
    theta = deg2rad(theta)

    theta, phi = meshgrid(theta, phi)

    # Calculation of the Beampattern
    BSA_max = 0

    w = ones(len(n))
    w = [0.9*exp(1j*deg2rad(136)), 0.3*exp(1j*deg2rad(0)), 1*exp(1j*deg2rad(271)), 1*exp(1j*deg2rad(283)), 0.9*exp(1j*deg2rad(279)), 0.3*exp(1j*deg2rad(54)), 1*exp(1j*deg2rad(128)), 1*exp(1j*deg2rad(136))]

    B = 0
    for k in range(0, len(n)):
        v_0 = exp(1j*2*pi*d*(sin(theta)*cos((phi_el*k) - phi)))  # Calculate the Array Manifold
        B += w[k]*v_0

    B = abs(B)


    ang = 70
    ang = deg2rad(ang)

    B_2 = 0
    for k in range(0, len(n)):
        v_0 = exp(1j * 2 * pi * d * (sin(ang) * cos((phi_el * k) - phi)))  # Calculate the Array Manifold
        B_2 += w[k]*v_0
    B_2 = abs(B_2)
    B_2 = 20*log10(B_2 / B.max())

    # Format 3D Plot
    bx = B*sin(theta)*cos(phi)
    by = B*sin(theta)*sin(phi)
    bz = B*cos(theta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot = ax.plot_surface(
        bx, by, bz, rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
        linewidth=0, antialiased=False, alpha=0.5)

    plt.ylabel('Y')
    plt.xlabel('X')
    plt.title('Plot')


    # Format Plot (Polar)
    fig = plt.figure()
    ax = plt.subplot(111, polar=True)
    plt.polar(phi, B_2, linewidth=1.0)
    ax.set_ylim(-30, 10)
    ax.set_yticks(array([-30, -20, -10, 0]))
    ax.set_xticks(array(deg2rad([-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150])))

    plt.show()


#snoi_gen(8, 1, 2, [20, 40], [20, 40])

if __name__ == "__main__": main()

