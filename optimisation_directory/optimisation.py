import numpy as np
import scipy

from circuit.circuit import circuit
from contraintes import EnergieDepenseParInstantSpatial, ContrainteNorme2Carre, ContrainteNormeInfini
from optimisation_directory.costFunction import CostFunction

# Options pour l'algorithme d'optimisation
Options = {
    "maxiter": 50,
    "disp": True,
    "eps": 0.25,
}

circui = circuit([1, 0, 0])
NBRE_SEGMENTS = circui.GetCircuitCoords().shape[0]
profile0 = [0 for i in range(NBRE_SEGMENTS)]
for i in range(int(NBRE_SEGMENTS/2)):
    profile0[2*i] = 10

# Formulation des optimisation : une contrainte sur l'énergie max sur tout le circuit et une contrainte sur la puissance
# disponible à un endroit du circuit
args = (circui,)

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


profile_opt = scipy.optimize.minimize(CostFunction, np.array(profile0), method='SLSQP', constraints=contraintes, options=Options, args=(circui,))
print(profile_opt.x)
print([val_profile ** 2 for val_profile in EnergieDepenseParInstantSpatial(profile_opt.x, circui)])
print(f'Energie totale du profil optimal : {sum([val_profile ** 2 for val_profile in EnergieDepenseParInstantSpatial(profile_opt.x, circui)])}')
