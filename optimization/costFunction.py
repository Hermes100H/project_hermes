from typing import List

from circuit.circuit_polynomial import Circuit
from optimization.pfd_solver import calculSolutions, calculVitesse
from utils.constants import CONST_g


def calcTimings(profile: List, circui: Circuit):
    vk = 0
    dx, dy = circui.GetDeltas()
    timings = list()
    for i in range(dy.shape[0]):
        acceleration = profile[i]
        vk, tsol, solved_solution = calculSolutions(dy[i], dx[i], vk, CONST_g, acceleration)
        vk, solved_vitesse = calculVitesse(tsol, vk, dy[i], dx[i], CONST_g, acceleration)
        if not solved_solution or not solved_vitesse:
            t = 100000
            timings.append(t)
            break
        timings.append(tsol)
    return timings


def CostFunction(profile: List, circui: Circuit):
    return sum(calcTimings(profile, circui))
