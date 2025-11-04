import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

# Tony Smoragiewicz
# August 2021
# VTOL drone design optimization

# Drag components from induced, parasitic, and form drag


def TotalDrag(S, b, Cl, Cd0, vel, rho):
    q = 0.5*rho*vel**2
    gamma = 1

    drag_body = q*0.2*0.02
    drag_ind = InducedDrag(S, b, Cl, Cd0, gamma, vel, rho)
    drag_para = ParasiticDrag(S, b, vel, rho)
    drag = drag_ind + drag_para + drag_body
    return drag

# Drag from skin friction


def ParasiticDrag(S, b, vel, rho):
    q = 0.5*rho*vel**2  # dynamic pressure
    mu = 1.75*10**-5    # dynamic viscosity
    c = S/b             # chord length
    Re = rho*vel*c/mu
    Re_x = 2*10**6      # Reynolds number for transition
    if Re < Re_x:
        Cf = 1.328/np.sqrt(Re)   # Laminar
    else:
        Cf = 0.027/(Re**(1/7))   # Turbulent

    # multiply by 2 for top and bottom of wing surface
    drag = 2*q*np.mean(Cf)*S
    return drag

# Lift induced drag


def InducedDrag(S, b, Cl, Cd0, gamma, vel, rho):
    q = 0.5*rho*vel**2  # dynamic pressure
    AR = b**2/S
    # fourth order polynomial fit to emperical data
    fxn = 0.0524*gamma**4 - 0.15*gamma**3 + 0.1659*gamma**2 - 0.0706*gamma + 0.0119
    e = 1/(1+fxn*AR)
    Cd_ind = Cd0 + Cl**2/(np.pi*AR*e)
    drag = q*Cd_ind*S
    return drag
