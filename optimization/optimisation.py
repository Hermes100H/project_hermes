import numpy as np
import scipy
import time

from circuit.circuit import Circuit
from contraintes import ContrainteNorme2Carre, ContrainteNormeInfini, EnergieDepenseParInstantSpatial
from optimization.costFunction import CostFunction, calcTimings
from optimization.csv_saver_optim import CSVsaver

# Options pour l'algorithme d'optimisation
options_slsqp = {
    "maxiter": 100,
    "disp": False,
    "eps": 0.1,
}

circui = Circuit(coeffs=[0, 1/12, 0], segment_length=1, starting_x=0, ending_x=20)
NBRE_SEGMENTS = circui.GetCircuitCoords().shape[0] - 1
profile0 = [0 for i in range(NBRE_SEGMENTS)]
for i in range(NBRE_SEGMENTS):
    profile0[i] = 3

# Formulation des optimisation : une contrainte sur l'énergie max sur tout le circuit et une contrainte sur la puissance
# disponible à un endroit du circuit
args = (circui,)
bounds = ((0, 10) for i in range(NBRE_SEGMENTS))

contraintes = [
    {"type": "ineq", "fun": ContrainteNorme2Carre, "args": args},
    {
        "type": "ineq",
        "fun": ContrainteNormeInfini,
    },
]

print(f"Nombre de points à considérer: {len(profile0)}")

def slsqp_optim_method():
    print("===================================================")
    print('\n\nOptimisation avec SLSQP')
    start = time.time()
    profile_opt_SLSQP = scipy.optimize.minimize(CostFunction, np.array(profile0), method='SLSQP', constraints=contraintes, options=options_slsqp, args=(circui,), bounds=bounds, tol=1e-6)
    end = time.time()
    print(f"Temps de calcul de l'optimisation SLSQP : {end - start} secondes")
    print("Profil de boost obtenu :")
    print(profile_opt_SLSQP.x)
    print(f"Temps pour parcourir le tracé avec le résultat de la méthode SLSQP : {profile_opt_SLSQP.fun}")
    print(EnergieDepenseParInstantSpatial(profile_opt_SLSQP.x, circui))
    print(calcTimings(profile_opt_SLSQP.x, circui))
    print(f'Energie totale du profil optimal : {sum(EnergieDepenseParInstantSpatial(profile_opt_SLSQP.x, circui))}')
    #CSVsaver(profile_opt_SLSQP.x, circui)

def Cobyla_optim_method():
    options_cobyla = {
        "rhobeg": 1.0,
        "disp": False,
        "maxiter": 100
    }
    start = time.time()
    profile_COBYLA = scipy.optimize.minimize(CostFunction, np.array(profile0), method='COBYLA', constraints=contraintes,
                                          options=options_cobyla, args=(circui,), tol=1e-6)
    end = time.time()
    print("===================================================")
    print('\n\nOptimisation avec COBYLA')
    print(f"Temps de calcul de l'optimisation COBYLA : {end - start} secondes")
    print("Profil de boost obtenu :")
    print(profile_COBYLA.x)
    print(f"Temps pour parcourir le tracé avec le résultat de la méthode COBYLA : {profile_COBYLA.fun}")
    print(EnergieDepenseParInstantSpatial(profile_COBYLA.x, circui))
    print(calcTimings(profile_COBYLA.x, circui))
    print(f'Energie totale du profil optimal : {sum(EnergieDepenseParInstantSpatial(profile_COBYLA.x, circui))}')
    #CSVsaver(profile_COBYLA.x, circui)


def trust_constr_optim_method():
    start = time.time()
    profile_trust_constr = scipy.optimize.minimize(CostFunction, np.array(profile0), method='trust-constr', constraints=contraintes,
                                             args=(circui,), tol=1e-6)
    end = time.time()
    print("===================================================")
    print('\n\nOptimisation avec trust-constr')
    print(f"Temps de calcul de l'optimisation trust-constr : {end - start} secondes")
    print("Profil de boost obtenu :")
    print(profile_trust_constr.x)
    print(f"Temps pour parcourir le tracé avec le résultat de la méthode trust-constr : {profile_trust_constr.fun}")
    print(EnergieDepenseParInstantSpatial(profile_trust_constr.x, circui))
    print(calcTimings(profile_trust_constr.x, circui))
    print(f'Energie totale du profil optimal : {sum(EnergieDepenseParInstantSpatial(profile_trust_constr.x, circui))}')
    # CSVsaver(profile_trust_constr.x, circui)

slsqp_optim_method()
Cobyla_optim_method()
trust_constr_optim_method()
