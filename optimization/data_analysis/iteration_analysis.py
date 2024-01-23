from typing import List, Union

import numpy as np
from matplotlib import pyplot as plt

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from optimization.contraintes import CarburantDepenseParInstantSpatial, DebitExpulsionSurLeCircuit
from optimization.costFunction import CostFunction
from utils.constants import TIME_ON_FAILURE


def store_iteration_data_step(profile: List, circuit: Union[Circuit, CircuitBspline], saved_results: List):
    saved_results.append((CostFunction(profile, circuit), profile, sum(CarburantDepenseParInstantSpatial(profile, circuit)), max(DebitExpulsionSurLeCircuit(profile, circuit))))


def store_iteration_data_step_friction(profile: List, circuit: Union[Circuit, CircuitBspline], saved_results: List):
    saved_results.append((CostFunction(profile, circuit, friction=True), profile, sum(CarburantDepenseParInstantSpatial(profile, circuit, friction=True)), max(DebitExpulsionSurLeCircuit(profile, circuit))))


def plot_iteration_steps(saved_results: List, block: bool):
    cost_values = list()
    profiles = list()
    energie = list()
    puissance = list()
    for val in saved_results:
        if val[0] > TIME_ON_FAILURE - 20:
            continue
        cost_values.append(val[0])
        profiles.append(val[1])
        energie.append(val[2])
        puissance.append(val[3])
    gradient = list()
    for i in range(len(profiles)-1):
        gradient.append(float(np.linalg.norm(profiles[len(profiles)-1]-profiles[i])))
    plt.figure()
    plt.plot(gradient)
    plt.show(block=False)
    plt.title("Gradient en norme 2 des profils de debit par rapport à la convergence en fonction des itérations")
    plt.xlabel('Itérations')
    plt.ylabel('Gradient entre le profil final et le profil à une certaine itération')
    plt.figure()
    plt.plot(cost_values)
    plt.title("Evolution de la fonction de coût (temps total du parcours) en fonction des itérations")
    plt.xlabel('Itérations')
    plt.ylabel('Valeur de la fonction de coût en secondes')
    plt.show(block=False)
    plt.figure()
    plt.plot(energie)
    plt.title("Evolution du carburant utilisé en fonction des itérations")
    plt.ylabel('Impulsion totale (en kg.m.s-1)')
    plt.xlabel('Itérations')
    plt.show(block=False)
    plt.figure()
    plt.plot(puissance)
    plt.title("Evolution du débit maximal donné en fonction des itérations")
    plt.ylabel('débit en kg.s-1')
    plt.xlabel('Itérations')
    plt.show(block=block)
