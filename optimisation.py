from typing import List

import numpy as np
import scipy

from ResolutionSystemePFD import calculSolutions, calculVitesse

PUISSANCE_ACCELERATION_MAXIMALE = 10.0  # m/(s**2) pour une voiture de 1500kg
QUANTITE_ENERGIE_ACCELERATION_MAXIMALE = 1000.0  # Energie disponible pour tout le circuit
NBRE_SEGMENTS = 10

def calcTiming(profile):
    t = 0
    vk = 0
    G = 10
    dx = 1
    dy = 1 / 12
    for i in range(NBRE_SEGMENTS):
        acceleration = profile[i]
        vk, tsol, solved_solution = calculSolutions(dy, dx, vk, G, acceleration)
        vk, solved_vitesse = calculVitesse(tsol, vk, dy, dx, G, acceleration)
        if not solved_solution or not solved_vitesse:
            t = 100000
            break
        t += tsol
    print(t)
    print(profile)
    return t


def ContrainteNorme2Carre(profile: List):
    """L'énergie 'dépensée' pour l'acceleration ne doit pas dépasser une certaine valeur sur le circuit"""
    return QUANTITE_ENERGIE_ACCELERATION_MAXIMALE-sum([val_profile ** 2 for val_profile in profile])


def ContrainteNormeInfini(profile: List):
    """La puissance maximale delivrée par la voiture à un instant t est limitée"""
    print(PUISSANCE_ACCELERATION_MAXIMALE - np.amax(profile))
    return PUISSANCE_ACCELERATION_MAXIMALE - max(profile)

# Formulation des contraintes : une contrainte sur l'énergie max sur tout le circuit et une contrainte sur la puissance
# disponible à un endroit du circuit
contraintes = [
    {
        'type': 'ineq',
        'fun': ContrainteNorme2Carre
    },
    {
        'type': 'ineq',
        'fun': ContrainteNormeInfini
    }
]

# Options pour l'algorithme d'optimisation
Options = {
    "maxiter": 25,
    "disp": True,
    "eps": 0.5,
}

profile0 = [0 for i in range(NBRE_SEGMENTS)]
for i in range(3):
    profile0[3*i] = 10

profile_opt = scipy.optimize.minimize(calcTiming, np.array(profile0), method='SLSQP', bounds=None, constraints=contraintes, options=Options)
