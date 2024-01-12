from typing import List

import numpy as np

from ResolutionSystemePFD import calculSolutions, calculVitesse
from constantes import PUISSANCE_ACCELERATION_MAXIMALE, ENERGIE_ACCELERATION_MAXIMALE, \
    NBRE_SEGMENTS


def EnergieDepenseParInstantSpatial(profile: List, dx: float, dy: float, G: float):
    """Calcul en fonction du profile et des temps d'acceleration sur le circuit de l'energie depensee"""
    valRen = list()
    vk = 0
    for i in range(NBRE_SEGMENTS):
        acceleration = profile[i]
        vk, tsol, solved_solution = calculSolutions(dy, dx, vk, G, acceleration)
        vk, solved_vitesse = calculVitesse(tsol, vk, dy, dx, G, acceleration)
        if not solved_solution or not solved_vitesse:
            tsol = 100000
            valRen.append(tsol)
            break
        valRen.append(acceleration * tsol)
    return valRen


def ContrainteNorme2Carre(profile: List, dx: float, dy: float, G: float):
    """L'énergie 'dépensée' pour l'acceleration ne doit pas dépasser une certaine valeur sur le circuit"""
    return ENERGIE_ACCELERATION_MAXIMALE-sum([energ ** 2 for energ in EnergieDepenseParInstantSpatial(profile, dx, dy, G)])


def ContrainteNormeInfini(profile: List):
    """La puissance maximale delivrée par la voiture à un instant t est limitée"""
    return PUISSANCE_ACCELERATION_MAXIMALE - max(profile)
