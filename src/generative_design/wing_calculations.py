import matplotlib.pyplot as plt
import numpy as np
from structures import moment_of_area, PolarMoment
from structures import point_load, uniform_load, triangle_load
from structures import distributed_torsion
from structures import torsion_strain, bending_strain

# Tony Smoragiewicz
# August 2021
# VTOL drone design optimization

# Reduce wall thickness until strain limit


def wing_strain(w, F, M, diameter, thickness, L, E, G):
    I = moment_of_area(diameter, thickness)
    J = PolarMoment(diameter, thickness)

    # Lifting by wingtips
    moment = point_load(F, L, E, I)
    # FAA Limit
    moment = uniform_load(w, L, E, I)
    # Twist angle from distributed torsion
    phi = distributed_torsion(M, L, J, G)
    phi_safe = distributed_torsion(M, L, J, G)

    # Maximum strains from bending and torsion
    strain_torsion = torsion_strain(M, J, diameter, G)
    strain_bending = bending_strain(moment, E, I, diameter)
    strain_total = np.sqrt(strain_bending**2 + strain_torsion**2)
    max_strain_percentage = strain_total/0.015*100
    return max_strain_percentage

# Minimize wing mass given:
# span, velocity, a/c mass, Cl, thickness ratio, air density


def wing_mass(ac_mass, b, q, Cl, Cm, tc):
    """Calculate the wing mass."""
    safety_factor = 1.5     # aerospace standard
    load_factor = 4.4       # FAA guideline
    g = 9.81                # gravitational acceleration

    span = ac_mass*g/(Cl*q)    # wing surface area
    aspect_ratio = b**2/span             # aspect ratio
    c = span/b                 # mean chord length
    L = b/2                 # Half wing span

    # Lifting loads
    w = -ac_mass*g/b*safety_factor*load_factor
    F = -ac_mass*g/2        # Lifting UAV by wingtips

    # Torsion moment from lift
    M = Cm*q*span/2*c*safety_factor*load_factor

    # Carbon Fiber
    E = 228*10**9           # Modulus of Elasticity
    G = 10*10**9            # Shear Modulus

    # Carbon Tube Geo
    print_thickness = 0.001                 # 3D printed airfoil thickness
    diameter = tc*c - 2*print_thickness     # carbon tube diameter
    diameter = np.floor(diameter*1000)/1000  # round down to nearest mm
    thickness = 0.0025                      # intial wall thickness

    # Reduce strut thickness to minimize weight
    max_strain = float('NaN')
    while True:

        # hard to find struts thinner than 5 mm
        if diameter <= 0.005:
            max_strain = float('NaN')
            break

        temp = wing_strain(w, F, M, diameter, thickness, L, E, G)

        # initial test is beyond strain limit
        if temp > 100.0 and np.isnan(max_strain):
            break
        # can still remove material
        elif temp <= 100.0 and thickness > 0.001:
            thickness = thickness-0.0005
            max_strain = temp
        # wall thickess less than or equal to 1.0 mm
        elif thickness <= 0.001:
            break
        elif temp > 100.0 and max_strain <= 100:
            thickness = thickness+0.0005
            break
        else:
            print('Wing Calculation else statement')
            break

    if np.isnan(max_strain):
        mass = float('NaN')
        aspect_ratio = float('NaN')
        span = float('NaN')
        max_strain = float('NaN')

    # 3D printed airfoil calculations
    volume = b*np.pi/4*(diameter**2 - (diameter-2*thickness)**2)
    density = 1750          # kg/m^3
    mass = density*volume
    mass = mass + span*2.320   # mass from 3D printed airfoil

    return mass, aspect_ratio, span, max_strain, thickness
