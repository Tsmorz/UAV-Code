from csv import reader
import numpy as np


def ReadInputs(__file__):
    constraints = []
    with open(__file__, newline='') as csvfile:
        filereader = reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            constraints = np.hstack([constraints, row[1]])
    constraints = constraints[1:]
    constraints = constraints.astype(float)
    return constraints
