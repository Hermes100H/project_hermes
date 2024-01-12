import numpy as np
import scipy

from ResolutionSystemePFD import calculSolutions, calculVitesse
from contraintes import EnergieDepenseParInstantSpatial, ContrainteNorme2Carre, ContrainteNormeInfini
from constantes import NBRE_SEGMENTS, G, dx, dy


def calcTiming(profile):
    t = 0
    vk = 0
    for i in range(NBRE_SEGMENTS):
        acceleration = profile[i]
        vk, tsol, solved_solution = calculSolutions(dy, dx, vk, G, acceleration)
        vk, solved_vitesse = calculVitesse(tsol, vk, dy, dx, G, acceleration)
        if not solved_solution or not solved_vitesse:
            t = 100000
            break
        t += tsol
    return t


# Formulation des optimisation_directory : une contrainte sur l'énergie max sur tout le circuit et une contrainte sur la puissance
# disponible à un endroit du circuit
args = (dx, dy, G,)

contraintes = [
    {
        'type': 'ineq',
        'fun': ContrainteNorme2Carre,
        'args': args
    },
    {
        'type': 'ineq',
        'fun': ContrainteNormeInfini,
    }
]

# Options pour l'algorithme d'optimisation_directory
Options = {
    "maxiter": 100,
    "disp": True,
    "eps": 0.25,
}

profile0 = [0 for i in range(NBRE_SEGMENTS)]
for i in range(3):
    profile0[3*i] = 3

profile_opt = scipy.optimize.minimize(calcTiming, np.array(profile0), method='SLSQP', constraints=contraintes, options=Options)
print(profile_opt.x)
print([val_profile ** 2 for val_profile in EnergieDepenseParInstantSpatial(profile_opt.x, dx, dy, G)])
print(f'Energie totale du profil optimal : {sum([val_profile ** 2 for val_profile in EnergieDepenseParInstantSpatial(profile_opt.x, dx, dy, G)])}')
