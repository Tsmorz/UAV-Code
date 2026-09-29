"""Hover power (disk loading) and take-off/landing energy requirements."""

import numpy as np

# power required to hover in watts


def hover_power(mass, diameter, num_of_props):
    """Power required to hover, in watts, from an empirical disk-loading fit."""
    disk_loading = [36.62, 2929.45]
    hovering_eff = [6.080, 0.608]
    curve = np.polyfit(np.log(disk_loading), hovering_eff, 1)

    area = num_of_props * np.pi * diameter**2 / 4
    prop_load = mass / area
    kg_kW = curve[0] * np.log(prop_load) + curve[1]
    power = mass / kg_kW * 1000  # convert to watts
    return power


def energy_take_off(power_hover, wing_area, rho):
    """Watt-hours to ascend to and descend from cruise altitude."""
    ascent = 4  # m/s
    descent = 3
    alt = 120  # meters
    Cd = 1.1  # flat plate
    # power drag from fuselage & wing
    power_climb = 0.5 * rho * Cd * (1.2 * wing_area) * ascent**3

    time_hr = alt / ascent / 60 / 60
    whr_ascent = 2 * time_hr * (power_hover + power_climb)

    time_hr = alt / descent / 60 / 60
    whr_descent = 2 * time_hr * power_hover

    whr = whr_ascent + whr_descent
    return whr
