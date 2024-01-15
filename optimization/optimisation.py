import numpy as np
import scipy

from circuit.circuit import Circuit
from contraintes import EnergieDepenseParInstantSpatial, ContrainteNorme2Carre, ContrainteNormeInfini
from optimization.costFunction import CostFunction, calcTimings
from optimization.csv_saver_optim import CSVsaver

# Options pour l'algorithme d'optimisation
Options = {
    "maxiter": 100,
    "disp": True,
    "eps": 0.25,
}

circui = Circuit(coeffs=[0, 1/12, 0], segment_length=1, starting_x=0, ending_x=10)
NBRE_SEGMENTS = circui.GetCircuitCoords().shape[0] - 1
profile0 = [0 for i in range(NBRE_SEGMENTS)]
for i in range(int(NBRE_SEGMENTS/3)):
    profile0[3*i] = 3

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
print(EnergieDepenseParInstantSpatial(profile_opt.x, circui))
print(calcTimings(profile_opt.x, circui))
print(f'Energie totale du profil optimal : {sum(EnergieDepenseParInstantSpatial(profile_opt.x, circui))}')
CSVsaver(profile_opt.x, circui)
