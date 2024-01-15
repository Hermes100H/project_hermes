from typing import List

from circuit.circuit import circuit
from optimization.costFunction import calcTimings

PUISSANCE_ACCELERATION_MAXIMALE = 10  # m/(s**2) pour une voiture de 1500kg
ENERGIE_ACCELERATION_MAXIMALE = 28  # Energie disponible pour tout le circuit

def EnergieDepenseParInstantSpatial(profile: List, circui: circuit):
    """Calcul en fonction du profile et des temps d'acceleration sur le circuit de l'energie depensee"""
    valRen = list()
    timings = calcTimings(profile, circui)
    for i in range(len(timings)):
        valRen.append((profile[i] * timings[i])**2)
    return valRen


def ContrainteNorme2Carre(profile: List, circui: circuit):
    """L'énergie 'dépensée' pour l'acceleration ne doit pas dépasser une certaine valeur sur le circuit"""
    return ENERGIE_ACCELERATION_MAXIMALE-sum(EnergieDepenseParInstantSpatial(profile, circui))
 

def ContrainteNormeInfini(profile: List):
    """La puissance maximale delivrée par la voiture à un instant t est limitée"""
    return PUISSANCE_ACCELERATION_MAXIMALE - max(profile)
