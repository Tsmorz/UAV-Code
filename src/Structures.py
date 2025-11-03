import matplotlib.pyplot as plt
import numpy as np

# Tony Smoragiewicz
# August 2021
# VTOL drone design optimization

# Second moment of area for hollow cylinder


def MomentOfArea(diameter, thickness):
    R1 = diameter/2
    R2 = (diameter-2*thickness)/2
    Ix = np.pi/4*(R1**4-R2**4)
    Iy = np.pi/4*(R1**4-R2**4)
    Iz = np.pi/4*(R1**4-R2**4)
    return Iz

# Polar moment of area for hollow cylinder


def PolarMoment(diameter, thickness):
    J = np.pi/32*(diameter**4 - (diameter-2*thickness)**4)
    return J

# Max moment from a point load wing tips


def PointLoad(F, L, E, I):
    x = np.arange(start=0, stop=L, step=0.1)
    delta = -F*x**2/(6*E*I)*(3*L - x)
    slope = -F*x/(2*E*I)*(2*L - x)
    moment = -F*(L - x)
    shear = F
    return max(moment)

# Max moment from a uniform distributed load


def UniformLoad(w, L, E, I):
    x = np.arange(start=0, stop=L, step=0.01)
    delta = -w*x**2/(24*E*I)*(6*L**2 - 4*L*x + x**2)
    slope = -w*x/(6*E*I)*(3*L**2 - 3*L*x + x**2)
    moment = -w*(L - x)**2/2
    shear = w*(L - x)
    '''
    plt.plot(x, delta, 'k-')
    plt.plot(-x, delta, 'k-')
    plt.xlabel('Span')
    plt.ylabel('Deflection')
    plt.axis('equal')
    plt.show()
    '''
    return max(moment)

# Max moment from a uniform distributed load


def TriangleLoad(p, L, E, I):
    x = np.arange(start=0, stop=L, step=0.01)
    delta = -p/(120*E*I*L)*x**2*(10*L**3 - 10*x*L**2 + 5*x**2*L - x**3)
    slope = -p/(24*E*I*L)*x*(4*L**3 - 6*x*L**2 + 4*x**2*L - x**3)
    moment = -p/(6*L)*(L - x)**3
    shear = p/(2*L)*(L - x)**2
    return max(moment)

# Twist angle from distributed torsion


def DistributedTorsion(M, L, J, G):
    Mx = M/L
    x = np.arange(start=0, stop=L, step=0.01)
    phi = Mx*x/(J*G)
    phi_deg = 180/np.pi*phi
    return phi_deg

# Maximum torsion strain


def TorsionStrain(M, J, diameter, G):
    r = diameter/2
    tau = M*r/J
    gamma = tau/G
    return gamma

# Maximum bending strain


def BendingStrain(M, E, Ic, diameter):
    c = diameter/2
    sigma = M*c/Ic  # stress
    epsilon = sigma/E  # strain
    return epsilon
