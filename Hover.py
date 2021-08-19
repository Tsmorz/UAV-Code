import matplotlib.pyplot as plt
import numpy as np

# power required to hover in watts
def PowerHover(mass, diameter, num_of_props):
    
    disk_loading = [36.62, 2929.45]
    hovering_eff = [6.080, 0.608]
    curve = np.polyfit(np.log(disk_loading), hovering_eff, 1)

    area = num_of_props*np.pi*diameter**2/4
    prop_load = mass/area
    kg_kW = curve[0]*np.log(prop_load) + curve[1]
    power = mass/kg_kW*1000 # convert to watts
    '''
    # Disk Loading vs Hovering Efficiency plot
    plt.figure()
    plt.semilogx(disk_loading, hovering_eff)
    plt.xlabel('Disk Loading (kg/m2)')
    plt.ylabel('Hovering Efficiency (kg/kW)')
    plt.grid(True, which="both")
    plt.show()

    print("The power requirement", round(power,1), "Watts")
    '''
    return power

def EnergyTakeOff(power_hover, wing_area, rho):
    ascent = 4  # m/s
    descent = 3
    alt = 120   # meters
    Cd = 1.1    # flat plate
    power_climb = 0.5*rho*Cd*(1.2*wing_area)*ascent**3 # power drag from fuselage & wing

    time_hr = alt/ascent/60/60
    whr_ascent = 2*time_hr*(power_hover+power_climb)
    
    time_hr = alt/descent/60/60
    whr_descent = 2*time_hr*power_hover
    
    whr = whr_ascent + whr_descent
    return whr

def EnergyHover(time, power):
    hr = time/60
    whr = hr*power
    return whr
