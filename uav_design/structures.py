"""Euler beam theory helpers: moments of area, beam loads, and strains."""

import matplotlib.pyplot as plt
import numpy as np

# Tony Smoragiewicz
# August 2021
# VTOL drone design optimization


def moment_of_area(diameter, thickness):
    """Second moment of area for a hollow cylinder."""
    radius_out = diameter / 2
    radius_in = (diameter - 2 * thickness) / 2
    Iz = np.pi / 4 * (radius_out**4 - radius_in**4)
    return Iz


def polar_moment(diameter, thickness):
    """Polar moment of area for a hollow cylinder."""
    J = np.pi / 32 * (diameter**4 - (diameter - 2 * thickness) ** 4)
    return J


def point_load(F, L, E, area_moment):
    """Max moment from a point load at the wing tips."""
    x: np.ndarray = np.arange(0.0, L, 0.1)
    moment = -F * (L - x)
    return max(moment)


def uniform_load(w, L, E, area_moment, plot: bool = False):
    """Max moment from a uniform distributed load."""
    x: np.ndarray = np.arange(0.0, L, 0.01)
    delta = -w * x**2 / (24 * E * area_moment) * (6 * L**2 - 4 * L * x + x**2)
    moment = -w * (L - x) ** 2 / 2
    if plot:
        plt.plot(x, delta, "k-")
        plt.plot(-x, delta, "k-")
        plt.xlabel("Span")
        plt.ylabel("Deflection")
        plt.axis("equal")
        plt.show()
    return max(moment)


def triangle_load(p, L, E, area_moment):
    """Max moment from a triangular distributed load."""
    x: np.ndarray = np.arange(0.0, L, 0.01)
    moment = -p / (6 * L) * (L - x) ** 3
    return max(moment)


def distributed_torsion(M, L, J, G):
    """Twist angle from distributed torsion."""
    Mx = M / L
    x: np.ndarray = np.arange(0.0, L, 0.01)
    phi = Mx * x / (J * G)
    phi_deg = 180 / np.pi * phi
    return phi_deg


def torsion_strain(M, J, diameter, G):
    """Maximum torsion strain."""
    r = diameter / 2
    tau = M * r / J
    gamma = tau / G
    return gamma


def bending_strain(M, E, Ic, diameter):
    """Maximum bending strain."""
    c = diameter / 2
    sigma = M * c / Ic  # stress
    epsilon = sigma / E  # strain
    return epsilon
