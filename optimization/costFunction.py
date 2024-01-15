from typing import List

from circuit.circuit import Circuit
from optimization.ResolutionSystemePFD import calculSolutions, calculVitesse
from optimization.constantes import G


def calcTimings(profile: List, circui: Circuit):
    vk = 0
    dx, dy = circui.GetDeltas()
    timings = list()
    for i in range(dy.shape[0]):
        acceleration = profile[i]
        vk, tsol, solved_solution = calculSolutions(dy[i], dx[i], vk, G, acceleration)
        vk, solved_vitesse = calculVitesse(tsol, vk, dy[i], dx[i], G, acceleration)
        if not solved_solution or not solved_vitesse:
            t = 100000
            timings.append(t)
            break
        timings.append(tsol)
    return timings


def CostFunction(profile: List, circui: Circuit):
    return sum(calcTimings(profile, circui))
