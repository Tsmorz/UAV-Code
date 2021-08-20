import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import axes3d
from ReadInputs import ReadInputs
from WingCalculations import WingMass
from AeroDrag import TotalDrag
from Hover import PowerHover, EnergyTakeOff

# Tony Smoragiewicz
# August 2021
# VTOL drone design optimization

__file__ = 'inputs.csv'
inputs = ReadInputs(__file__)       # Read inputs from csv file
mass = inputs[0]                    # Aircraft total mass
overall_span = inputs[1]            # tip to tip of propellors
useable_span = 0.9*overall_span     # a/c body is 10% of span
vel = np.arange(15, 45.1, 0.25)     # meters/s          
# wing_span = np.arange(0.5*useable_span, 2*useable_span, 0.01) # meters
wing_span = np.arange(0.5*useable_span, 0.9*useable_span, 0.01)  # meters
num_props = 2

# Airfoils Parameters
Cl_max = inputs[2]/0.95             # Lift coefficient - max
Cl = inputs[3]/0.95                 # Lift coefficient - cruise
Cd0 = inputs[4]                     # Drag coefficient - cruise
Cm = inputs[5]                      # Moment coefficient - maximum
tc = inputs[6]                      # thickness ratio (thickness/chord)

##########################################################################
### --- DON'T EDIT BELOW THIS LINE --- ###################################
##########################################################################

# Atmospheric Conditions
p = 101*10**3                       # pressure
C = 25                              # temp in Celius
R = 287.058                         # gas constant J/kg/K
T = 273 + C                         # temp in Kelvin
rho = p/(R*T)                       # air density
q = 1/2*rho*vel**2                  # dynamic pressure
g = 9.81

wing_mass = np.zeros((len(wing_span), len(q)))
wing_AR = np.zeros((len(wing_span), len(q)))
wing_area = np.zeros((len(wing_span), len(q)))
wing_strain = np.zeros((len(wing_span), len(q)))
wing_t = np.zeros((len(wing_span), len(q)))

# Calculate wing parameters
print("Calculating structure...")
for i in range(len(wing_span)):
    for j in range(len(q)):
        m, AR, S, strain, thickness = WingMass(
            mass, wing_span[i], q[j], Cl, Cm, tc)
        wing_mass[i][j] = m
        wing_AR[i][j] = AR
        wing_area[i][j] = S
        wing_strain[i][j] = strain
        wing_t[i][j] = thickness

wing_mass = wing_mass.T
wing_AR = wing_AR.T
wing_area = wing_area.T
wing_strain = wing_strain.T
wing_t = wing_t.T

wing_span, q = np.meshgrid(wing_span, q)
vel = np.sqrt(2*q/rho)
prop_diameter = useable_span-wing_span

# Calculate aero drag parameters
print("Calculating drag...")
print()
power_drag = np.zeros(wing_mass.shape)
hover_whr = np.zeros(wing_mass.shape)
r, c = power_drag.shape
for i in range(r):
    for j in range(c):
        total = TotalDrag(wing_area[i][j], wing_span[i]
                          [j], Cl, Cd0, vel[i][j], rho)
        power_drag[i][j] = vel[i][j]*total
        power_hover = PowerHover(mass, prop_diameter[i][j], num_props)
        hover_whr[i][j] = EnergyTakeOff(power_hover, wing_area[i][j], rho)

# Battery parameters
batt_mass = 0.35*mass-wing_mass
batt_whr = 120*batt_mass
batt_cost = batt_whr/1.56

# Max hover time
hover_time = 0

# Flight Range
duration = (batt_whr-hover_whr)*60*60/power_drag
distance = vel/1000 * duration
idx = np.isnan(wing_strain)
distance[idx] = float('NaN')
max_distance = np.nanmax(distance)
max_distance99 = np.where(distance >= 0.98*(max_distance))

km_per_whr = distance/batt_whr
km_per_kwhr = km_per_whr*1000
dollar_per_kwhr = 0.21  # euro per kwh
km_per_dollar = km_per_kwhr/dollar_per_kwhr
max_km_per_dollar = np.nanmax(km_per_dollar)

# Final Outputs
ind = np.unravel_index(np.nanargmax(distance, axis=None), distance.shape)
AR = wing_AR[ind]
S = wing_area[ind]
b = wing_span[ind]
c = S/b
prop_diam = prop_diameter[ind]
spar = np.floor(1000*(c*tc - 2*0.001))/1000
thickness = wing_t[ind]
cruise = vel[ind]
stall = np.sqrt(2*mass*g/(rho*S*Cl_max))
kwhr = batt_whr[ind]/1000
##########################################################################
### --- Write A/C details to terminal --- ################################
##########################################################################

print("Tiltrotor Details:")
print("-----------------------------------")
print("Flight radius:\t\t",     round(max_distance/2, 2), "km")
print("Hover time:\t\t",        hover_time, "min")
print("Total Mass:\t\t",        round(mass, 3), "kg")
print("Total Width:\t\t",       round(overall_span, 2), "m")
print()
print("Aspect Ratio:\t\t",      round(AR, 1))
print("Wing Area:\t\t",         round(S, 3), "m2")
print("Wing Span:\t\t",         round(b, 3), "m")
print("Chord:\t\t\t",           round(c, 3), "m")
print("Spar:\t\t\t",            1000*spar, "mm")
print("Spar thickness:\t\t",    thickness*1000, 'mm')
print()
print("Prop Diameter:\t\t",     round(prop_diam, 3), "m")
print("Span to Prop Ratio:\t",  round(b/prop_diam, 2))
print()
print("Air density:\t\t",       round(rho, 3), "kg/m3")
print("Cruise Velocity:\t",     round(cruise, 2), "m/s")
print("Stall Velocity:\t\t",    round(1.2*stall, 2),"m/s")
print()
print("Battery size:\t\t",      round(kwhr, 3), "kwhr")

##########################################################################
### --- Plot Data --- ####################################################
##########################################################################

# Flight Radius
plt.subplot(121)
CS = plt.contour(wing_span, vel, distance/max_distance, 50)
'''
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
CS = plt.contour(wing_span,vel,wing_AR, 10)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
'''
plt.plot(wing_span[max_distance99], vel[max_distance99], 'bo')
plt.plot(wing_span[ind], vel[ind], 'ro')
plt.title('Range (km)')
plt.xlabel('Wing Span (m)')
plt.ylabel('Vel (m/s)')

# Wing Loading
plt.subplot(122)
CS = plt.contour(wing_span, vel, hover_whr/batt_whr, 20)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
CS = plt.contour(wing_span, vel, prop_diameter, 10)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
plt.title('Power Drag')
plt.xlabel('Span (m)')
plt.ylabel('Vel (m/s)')

plt.show()