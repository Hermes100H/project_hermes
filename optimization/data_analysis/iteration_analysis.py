from typing import List, Union

import numpy as np
from matplotlib import pyplot as plt

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from optimization.contraintes import EnergieDepenseParInstantSpatial
from optimization.costFunction import CostFunction
from utils.constants import TIME_ON_FAILURE


def store_iteration_data_step(profile: List, circuit: Union[Circuit, CircuitBspline], saved_results: List):
    saved_results.append((CostFunction(profile, circuit), profile, sum(EnergieDepenseParInstantSpatial(profile, circuit))))


def plot_iteration_steps(saved_results: List, block: bool):
    cost_values = list()
    profiles = list()
    energie = list()
    for val in saved_results:
        if val[0] > TIME_ON_FAILURE - 20:
            continue
        cost_values.append(val[0])
        profiles.append(val[1])
        energie.append(val[2])
    gradient = list()
    for i in range(len(profiles)-1):
        gradient.append(float(np.linalg.norm(profiles[len(profiles)-1]-profiles[i])))
    plt.figure()
    plt.plot(gradient)
    plt.show(block=False)
    plt.title("Gradient des profils de boost par rapport à la convergence en fonction des itérations")
    plt.xlabel('Itérations')
    plt.ylabel('Gradient entre le profil final et le profil à une certaine itération')
    plt.figure()
    plt.plot(cost_values)
    plt.title("Evolution de la fonction de coût en fonction des itérations")
    plt.xlabel('Itérations')
    plt.ylabel('Valeur de la fonction de coût en secondes')
    plt.show(block=False)
    plt.figure()
    plt.plot(energie)
    plt.title("Evolution de l'énergie en fonction des itérations")
    plt.ylabel('Energie en joules')
    plt.xlabel('Itérations')
    plt.show(block=block)
