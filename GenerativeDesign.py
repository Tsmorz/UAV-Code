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
if mass > 24.95:                    # FAA limit is 55lbs
    mass = 24.95
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
power_hover = np.zeros(wing_mass.shape)
hover_whr = np.zeros(wing_mass.shape)
r, c = power_drag.shape
for i in range(r):
    for j in range(c):
        total = TotalDrag(wing_area[i][j], wing_span[i]
                          [j], Cl, Cd0, vel[i][j], rho)
        power_drag[i][j] = vel[i][j]*total
        power_hover[i][j] = PowerHover(mass, prop_diameter[i][j], num_props)
        hover_whr[i][j] = EnergyTakeOff(power_hover[i][j], wing_area[i][j], rho)

# Battery parameters
batt_mass = 0.35*mass-wing_mass
batt_whr = 120*batt_mass
batt_cost = batt_whr/1.56
batt_whr = batt_whr - hover_whr

# Max hover time
hover_time = batt_whr/power_hover*60 # hover time in minutes

# Flight Range
duration = batt_whr/power_drag*60*60 # flight time in seconds
distance = vel/1000 * duration
idx = np.isnan(wing_strain)
distance[idx] = float('NaN')
hover_time[idx] = float('NaN')
max_distance = np.nanmax(distance)
max_distance99 = np.where(distance >= 0.98*(max_distance))

km_per_whr = distance/batt_whr
km_per_kwhr = km_per_whr*1000
dollar_per_kwhr = 0.21  # euro per kwh
km_per_dollar = km_per_kwhr/dollar_per_kwhr
max_km_per_dollar = np.nanmax(km_per_dollar)

# Final Outputs
ind = np.unravel_index(np.nanargmax(distance, axis=None), distance.shape)
max_hover_ind = np.unravel_index(np.nanargmax(hover_time, axis=None), distance.shape)
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
data = [["Flight radius:",round(max_distance/2, 2), "km"],
["Hover time:", round(hover_time[ind],1), "min"],
["Total Mass:", round(mass, 3), "kg"],
["Total Width:", round(overall_span, 2), "m"],
["Aspect Ratio:", round(AR, 1), ""],
["Wing Area:", round(S, 3), "m2"],
["Wing Span:", round(b, 3), "m"],
["Chord:", round(c, 3), "m"],
["Spar:", 1000*spar, "mm"],
["Thickness:", thickness*1000, 'mm'],
["Prop Diameter:", round(prop_diam, 3), "m"],
["Span to Prop Ratio:", round(b/prop_diam, 2), ""],
["Air density:", round(rho, 3), "kg/m3"],
["Cruise Velocity:", round(cruise, 2), "m/s"],
["Stall Velocity:", round(1.2*stall, 2),"m/s"],
["Battery size:", round(kwhr, 3), "kwhr"]]

dash = '-' * 40
print("Tiltrotor Details:")
print(dash)

for i in range(len(data)):
    print('{:<23s}{:^6.2f}{:<10s}'.format(data[i][0],data[i][1],data[i][2]))

##########################################################################
### --- Plot Data --- ####################################################
##########################################################################

# Flight Radius
plt.subplot(121)
levels = max_distance/2*np.array([0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.05])
CS = plt.contour(wing_span, vel, distance/2, levels)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
plt.plot(wing_span[ind], vel[ind], 'ro')
CS = plt.contour(wing_span, vel, prop_diameter, 5)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
plt.title('Flight Radius (km)')
plt.xlabel('Wingspan (m)')
plt.ylabel('Vel (m/s)')

# Hover Time
plt.subplot(122)
levels = hover_time[max_hover_ind]*np.array([0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.05])
CS = plt.contour(wing_span, vel, hover_time, levels)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
plt.plot(wing_span[max_hover_ind], vel[max_hover_ind], 'ro')
CS = plt.contour(wing_span, vel, prop_diameter/b, 5)
plt.clabel(CS, CS.levels, inline=True, fontsize=10)
plt.title('Max Hover Time (min)')
plt.xlabel('Wingspan (m)')
plt.ylabel('Vel (m/s)')

plt.show()