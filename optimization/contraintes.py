from typing import List

from circuit.circuit_polynomial import Circuit
from optimization.costFunction import calcTimings, compute_times_with_air_friction
from utils.constants import DEBIT_EXPULSION_MAXIMAL, M_CARBURANT


# modèle : F = m0(x) * Ve,      avec Ve vitesse d'expulsion de gaz (m.s-1) et m0(x) débit de sortie du gaz (kg.s-1)
def CarburantDepenseParInstantSpatial(profile: List, circui: Circuit, friction: bool = False):
    """Calcul en fonction du profile et des temps d'acceleration sur le circuit de l'energie depensee"""
    valRen = list()
    timings = calcTimings(profile, circui, friction)
    for i in range(len(timings)):
        valRen.append(profile[i] * timings[i])
    return valRen


def ContrainteNorme2Carre(profile: List, circui: Circuit, friction: bool = False):
    """L'énergie 'dépensée' pour l'acceleration ne doit pas dépasser une certaine valeur sur le circuit"""
    contrainte = M_CARBURANT - sum(CarburantDepenseParInstantSpatial(profile, circui, friction=friction))
    print(contrainte)
    print(profile)
    return contrainte


def DebitExpulsionSurLeCircuit(profile: List, circui: Circuit):
    return profile


def ContrainteNormeInfini(profile: List, circui: Circuit):
    """La puissance maximale delivrée par la voiture à un instant t est limitée"""
    return DEBIT_EXPULSION_MAXIMAL - max(DebitExpulsionSurLeCircuit(profile, circui))
