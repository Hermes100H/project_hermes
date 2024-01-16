import numpy as np
import scipy
import time

from circuit.circuit import Circuit
from contraintes import ContrainteNorme2Carre, ContrainteNormeInfini
from optimization.costFunction import CostFunction
from optimization.csv_saver_optim import CSVsaver, print_optim_info

circuit = Circuit(coeffs=[1/100, 0, 0], segment_length=1, starting_x=0, ending_x=10)
NBRE_SEGMENTS = circuit.GetCircuitCoords().shape[0] - 1
profile0 = [0 for i in range(NBRE_SEGMENTS)]
for i in range(NBRE_SEGMENTS):
    profile0[i] = 3

args = (circuit,)
tol = 1e-6
bounds = ((0, 10) for i in range(NBRE_SEGMENTS))

contraintes = [
    {"type": "ineq", "fun": ContrainteNorme2Carre, "args": args},
    {
        "type": "ineq",
        "fun": ContrainteNormeInfini,
    },
]

print(f"Nombre de points à considérer: {len(profile0)}")

options_slsqp = {
    "maxiter": 100,
    "disp": True,
    "eps": 0.1,
}

options_cobyla = {
    "rhobeg": 1.0,
    "disp": True,
    "maxiter": 100
}

options_trust_constr ={
    "disp": True,
}


def optim(optim_method, profile0, contraintes, args, tol, option, bounds, circuit):
    start = time.time()
    if optim_method == 'SLSQP':
        profile_opt = scipy.optimize.minimize(CostFunction, np.array(profile0), method=optim_method,
                                                    constraints=contraintes, options=option, args=args,
                                                    bounds=bounds, tol=tol)
    else:
        profile_opt = scipy.optimize.minimize(CostFunction, np.array(profile0), method=optim_method,
                                                 constraints=contraintes,
                                                 options=option, args=args, tol=tol)
    end = time.time()
    print_optim_info(profile_opt, circuit, optim_method)
    print(f"Temps de calcul de l'optimisation {optim_method} : {end - start} secondes")
    # CSVsaver(profile_opt.x, circuit)


optim('SLSQP', profile0, contraintes, args, tol, options_slsqp, bounds, circuit)
optim('COBYLA', profile0, contraintes, args, tol, options_cobyla, bounds, circuit)
optim('trust-constr', profile0, contraintes, args, tol, options_trust_constr, bounds, circuit)
