import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import axes3d
from WingCalculations import WingMass
from AeroDrag import TotalDrag
from Hover import PowerHover, EnergyHover, EnergyTakeOff

# Tony Smoragiewicz
# August 2021
# VTOL drone design optimization

# Aircraft total mass
mass = 4/0.25

# Wing span and velocities to search over
overall_span = 1.85             # tip to tip of propellors
useable_span = 0.9*overall_span  # a/c body is 10% of span
vel = np.arange(15, 45.1, 0.25)  # meters/sec
updown = 1                      # number of times UAV can take off and land
hover_time = 5                  # minutes

# Airfoils Parameters @ cruise
# NACA 25112
Cl = 1.1    # Lift coefficient - cruise
Cl = Cl/0.95
Cl_max = 1.55
Cd0 = 0.02  # Drag coefficient - cruise
Cm = 0.03   # Moment coefficient - maximum
tc = 0.14   # thickness ratio (thickness/chord)

##########################################################################
### --- DON'T EDIT BELOW THIS LINE --- ###################################
##########################################################################

# Atmospheric Conditions
p = 101*10**3       # pressure
C = 25              # temp in Celius
R = 287.058         # gas constant J/kg/K
T = 273 + C         # temp in Kelvin
rho = p/(R*T)       # air density
q = 1/2*rho*vel**2  # dynamic pressure
g = 9.81

# wing_span = np.arange(0.5*useable_span, 2*useable_span, 0.01) # meters
wing_span = np.arange(0.5*useable_span, 0.9*useable_span, 0.01)  # meters
num_props = 2

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
total_whr = np.zeros(wing_mass.shape)
r, c = power_drag.shape
for i in range(r):
    for j in range(c):
        total = TotalDrag(wing_area[i][j], wing_span[i]
                          [j], Cl, Cd0, vel[i][j], rho)
        power_drag[i][j] = vel[i][j]*total
        power_hover = PowerHover(mass, prop_diameter[i][j], num_props)
        # print(power_hover)
        takeoff = EnergyTakeOff(power_hover, wing_area[i][j], rho)
        hover = EnergyHover(hover_time, power_hover)
        total_whr[i][j] = updown*takeoff + hover

# print(total_whr)
# Battery parameters
batt_mass = 0.35*mass-wing_mass
batt_whr = 120*batt_mass
batt_cost = batt_whr/1.56

# Flight Range
duration = (batt_whr-total_whr)*60*60/power_drag
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

ind = np.unravel_index(np.nanargmax(distance, axis=None), distance.shape)

##########################################################################
### --- Write A/C details to terminal --- ################################
##########################################################################

print("Tiltrotor Details:")
print("-----------------------------------")
print("Flight radius:\t\t",     round(distance[ind]/2, 2), "km")
print("Hover time:\t\t",        hover_time, "min")
print("Total Mass:\t\t",        round(mass, 3), "kg")
print("Total Width:\t\t",       round(overall_span, 2), "m")
print()
print("Aspect Ratio:\t\t",      round(wing_AR[ind], 1))
print("Wing Area:\t\t",         round(wing_area[ind], 3), "m2")
print("Wing Span:\t\t",         round(wing_span[ind], 3), "m")
print("Chord:\t\t\t",           round(wing_span[ind]/wing_AR[ind], 3), "m")
print("Spar:\t\t\t",            np.floor(
    1000*(wing_area[ind]/wing_span[ind]*tc - 2*0.001)), "mm")
print("Spar thickness:\t\t",    round(wing_t[ind]*1000, 3), 'mm')
print()
print("Prop Diameter:\t\t",     round(prop_diameter[ind], 3), "m")
print("Span to Prop Ratio:\t",  round(wing_span[ind]/prop_diameter[ind], 2))
print()
print("Air density:\t\t",       round(rho, 3), "kg/m3")
print("Cruise Velocity:\t",     round(vel[ind], 2), "m/s")
print("Stall Velocity:\t\t",    round(np.sqrt(2*mass*g/(rho*wing_area[ind]*Cl_max)),2),"m/s")
print()
print("Battery size:\t\t",      round(batt_whr[ind]/1000, 3), "kwhr")

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
CS = plt.contour(wing_span, vel, total_whr/batt_whr, 20)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
CS = plt.contour(wing_span, vel, prop_diameter, 10)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
plt.title('Power Drag')
plt.xlabel('Span (m)')
plt.ylabel('Vel (m/s)')

plt.show()
