import matplotlib.pyplot as plt
import numpy as np

wing_loading = [26.85, 3417.70]
hovering_eff = [6.08, 0.85]
curve = np.polyfit(np.log(wing_loading), hovering_eff, 1)


# Wing Loading vs Hovering Efficiency plot
plt.figure()
plt.subplot(221)
plt.semilogx(wing_loading, hovering_eff)
plt.xlabel('Disk Loading (kg/m2)')
plt.ylabel('Hovering Efficiency (kg/kW)')
plt.grid(True, which="both")

'''
# Drone hover power usage
mass = .430
prop_diam = 0.13
prop_num = 4
area = prop_num*np.pi*prop_diam**2/4
prop_load = mass/area

y = curve[0]*np.log(prop_load) + curve[1]
power = mass/y*1000
print(power)
'''

# Propeller area used
prop_num = np.array([1, 2, 3, 4, 5, 6, 7, 8])
factor = np.array([1.0, 0.5, 0.464, 0.414, 0.370, 0.333, 0.303, 0.277])
diam = np.sqrt(4/np.pi)
area = prop_num*np.pi*(factor*diam)**2/4
#print(area)

plt.subplot(222)
plt.plot(prop_num,area)
plt.plot(prop_num,factor*diam)
plt.xlabel('# of propellers')
plt.ylabel('Area used/available')


b = 1.85
c = b/10
S = b*c
AR = b**2/S

alpha = np.arange(start=0, stop=16, step=2.5)
vel = np.arange(start=0, stop=45, step=0.01)

# Airfoil E216
Cl = np.array([0.6, 1.0, 1.25, 1.45, 1.55, 1.55, 1.55])
e=1.78*(1-0.045*AR**0.68)-0.64
Cd = np.array([20, 15, 15, 20, 30, 60, 100])/1000


# Design Trafeoff - QUAD v VTOL v WING
payload = 1.5#1.8
mass = payload/0.2
g = 9.81
rho = 1.15
print("Wing Loading", round(mass/S,2))

# Fixed Wing a/c

area_fuselage = np.pi*(b/10)**2/4
Cd_fuselage = 0.2
Cl = 1.5
Lift = 0.5*rho*Cl*S*vel**2
WING_drag = Lift/10 #.5*rho*(Cd[0]*S+Cd_fuselage*area_fuselage)*vel**2
WING_power = WING_drag*vel

Cl = 1.5
v_stall = np.sqrt(2*mass*g/(rho*Cl*S))
print("Vstall", round(v_stall,2))
Cl = 1.1
v_cruise = np.sqrt(2*mass*g/(rho*Cl*S))
v_cruise = round(v_cruise,2)
print("Vcruise", v_cruise)

# Quadrotor
num_props = 4
diam_props = b*factor[num_props-1]
Cd = 1.5
QUAD_area = np.sqrt(2*(b-diam_props))*0.015
QUAD_drag = 2*0.5*rho*Cd*QUAD_area*vel**2

Thrust = np.sqrt(QUAD_drag**2 + (mass*g)**2)
area = num_props*np.pi*diam_props**2/4
prop_load = Thrust/g/area
y = curve[0]*np.log(prop_load) + curve[1]
QUAD_power = mass/y*1000 + QUAD_drag*vel

#VTOL
num_props = 4
diam_props = 0.16*b

Thrust = mass*g - Lift
area = num_props*np.pi*diam_props**2/4
prop_load = Thrust/g/area
VTOL_power = np.zeros(len(vel))
for i in range(len(VTOL_power)):
    if Thrust[i]>0:
        y = curve[0]*np.log(prop_load[i]) + curve[1]
        VTOL_power[i] = mass/y*1000 + WING_power[i]*1.5
    else:
        VTOL_power[i] = WING_power[i]*1.5

plt.subplot(223)
plt.plot(vel, WING_power)
plt.plot(vel, QUAD_power)
plt.plot(vel, VTOL_power)
plt.xlabel('Vel (m/s)')
plt.ylabel('Power (W)')
plt.xlim([0, v_cruise])
plt.ylim([0, 1750])

plt.subplot(224)
plt.plot(vel, prop_load)
plt.ylim([0, 20])


#Battery Calc
Whr_total = 200 * 0.35*mass # 200 Whr/kg

Ascent = 4 # m/s
Descent = 3
Alt = 120 # meters

P_climb = 0.5*rho*(1.1*S*1.2)*Ascent**3 # power drag from fuselage & wing

Whr_ascent = 2*Alt/Ascent*(VTOL_power[0]+P_climb)/60/60
Whr_descent = 2*Alt/Descent*VTOL_power[0]/60/60
Whr_vertical = Whr_ascent + Whr_descent
print(Whr_total)
print(Whr_vertical)

ind = np.where(vel == v_cruise)
VTOL_power_cruise = VTOL_power[ind]
Time_at_cruise = (Whr_total-Whr_vertical)/VTOL_power_cruise
Range = v_cruise*Time_at_cruise/1000*60*60
print("VTOL range", Range)

plt.show()
