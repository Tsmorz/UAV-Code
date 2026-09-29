"""Read the aircraft design constraints from a CSV file."""

from csv import reader

import numpy as np


def read_inputs(path):
    """Parse the constraint values from the second column of ``path``."""
    constraints = []
    with open(path, newline="") as csvfile:
        filereader = reader(csvfile, delimiter=",", quotechar="|")
        for row in filereader:
            constraints = np.hstack([constraints, row[1]])
    constraints = constraints[1:]
    constraints = constraints.astype(float)
    return constraints
