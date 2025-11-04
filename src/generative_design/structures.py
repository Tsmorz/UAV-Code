import matplotlib.pyplot as plt
import numpy as np

# Tony Smoragiewicz
# August 2021
# VTOL drone design optimization

def moment_of_area(diameter, thickness):
    """Second moment of area for hollow cylinder."""
    radius_out = diameter/2
    radius_in = (diameter-2*thickness)/2
    Ix = np.pi/4*(radius_out**4-radius_in**4)
    Iy = np.pi/4*(radius_out**4-radius_in**4)
    Iz = np.pi/4*(radius_out**4-radius_in**4)
    return Iz

def PolarMoment(diameter, thickness):
    """Polar moment of area for hollow cylinder."""
    J = np.pi/32*(diameter**4 - (diameter-2*thickness)**4)
    return J

def point_load(F, L, E, I):
    """Max moment from a point load wing tips."""
    x = np.arange(start=0, stop=L, step=0.1)
    delta = -F*x**2/(6*E*I)*(3*L - x)
    slope = -F*x/(2*E*I)*(2*L - x)
    moment = -F*(L - x)
    shear = F
    return max(moment)


def uniform_load(w, L, E, I, plot:bool=False):
    """Max moment from a uniform distributed load."""
    x = np.arange(start=0, stop=L, step=0.01)
    delta = -w*x**2/(24*E*I)*(6*L**2 - 4*L*x + x**2)
    slope = -w*x/(6*E*I)*(3*L**2 - 3*L*x + x**2)
    moment = -w*(L - x)**2/2
    shear = w*(L - x)
    if plot:
        plt.plot(x, delta, 'k-')
        plt.plot(-x, delta, 'k-')
        plt.xlabel('Span')
        plt.ylabel('Deflection')
        plt.axis('equal')
        plt.show()
    return max(moment)


def triangle_load(p, L, E, I):
    """Max moment from a uniform distributed load."""
    x = np.arange(start=0, stop=L, step=0.01)
    delta = -p/(120*E*I*L)*x**2*(10*L**3 - 10*x*L**2 + 5*x**2*L - x**3)
    slope = -p/(24*E*I*L)*x*(4*L**3 - 6*x*L**2 + 4*x**2*L - x**3)
    moment = -p/(6*L)*(L - x)**3
    shear = p/(2*L)*(L - x)**2
    return max(moment)

def distributed_torsion(M, L, J, G):
    """Twist angle from distributed torsion."""
    Mx = M/L
    x = np.arange(start=0, stop=L, step=0.01)
    phi = Mx*x/(J*G)
    phi_deg = 180/np.pi*phi
    return phi_deg

def torsion_strain(M, J, diameter, G):
    """Maximum torsion strain."""
    r = diameter/2
    tau = M*r/J
    gamma = tau/G
    return gamma


def bending_strain(M, E, Ic, diameter):
    """Maximum bending strain."""
    c = diameter/2
    sigma = M*c/Ic  # stress
    epsilon = sigma/E  # strain
    return epsilon
