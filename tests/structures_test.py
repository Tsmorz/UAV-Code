"""Smoke tests for the structural helper functions."""

import numpy as np

from uav_design.structures import moment_of_area, polar_moment


def test_moment_of_area_matches_hollow_cylinder_formula():
    """moment_of_area matches the closed-form hollow-cylinder result."""
    diameter, thickness = 0.02, 0.002
    radius_out = diameter / 2
    radius_in = (diameter - 2 * thickness) / 2
    expected = np.pi / 4 * (radius_out**4 - radius_in**4)
    assert moment_of_area(diameter, thickness) == expected


def test_polar_moment_is_twice_the_area_moment():
    """For a thin hollow cylinder, J = Ix + Iy = 2 * I."""
    diameter, thickness = 0.02, 0.002
    assert polar_moment(diameter, thickness) == 2 * moment_of_area(diameter, thickness)
