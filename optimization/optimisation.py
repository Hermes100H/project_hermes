import time

import numpy as np
import scipy

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from contraintes import ContrainteNorme2Carre, ContrainteNormeInfini
from optimization.costFunction import CostFunction
from optimization.csv_saver_optim import CSVsaver, print_optim_info


def init_circuit():
    circuit = Circuit(coeffs=[1 / 100, 0, 0], segment_length=1, starting_x=0, ending_x=10)
    return circuit


def init_circuit_spline():
    circuit = CircuitBspline(dx_length=0.1)
    circuit.plot_spline()
    return circuit


def init_profile(circuit: Circuit):
    nbre_segments = circuit.GetCircuitCoords().shape[0] - 1
    profile0 = [0 for i in range(nbre_segments)]
    for i in range(int(nbre_segments / 2)):
        profile0[i] = 10
    return profile0


def init_args_optim(circuit):
    nbre_segments = circuit.GetCircuitCoords().shape[0] - 1
    args = (circuit,)
    tol = 1e-6
    bounds = ((0, 10) for i in range(nbre_segments))
    contraintes = [
        {"type": "ineq", "fun": ContrainteNorme2Carre, "args": args},
        {
            "type": "ineq",
            "fun": ContrainteNormeInfini,
        },
    ]

    options_slsqp = {
        "maxiter": 100,
        "disp": True,
        "eps": 0.1,
    }

    options_cobyla = {"rhobeg": 1.0, "disp": True, "maxiter": 100}

    options_trust_constr = {
        "disp": True,
    }
    return args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla


def optim(optim_method, profile0, contraintes, args, tol, option, bounds, circuit):
    start = time.time()
    if optim_method == "SLSQP":
        profile_opt = scipy.optimize.minimize(
            CostFunction,
            np.array(profile0),
            method=optim_method,
            constraints=contraintes,
            options=option,
            args=args,
            bounds=bounds,
            tol=tol,
        )
    else:
        profile_opt = scipy.optimize.minimize(
            CostFunction,
            np.array(profile0),
            method=optim_method,
            constraints=contraintes,
            options=option,
            args=args,
            tol=tol,
        )
    end = time.time()
    print_optim_info(profile_opt, circuit, optim_method)
    print(f"Temps de calcul de l'optimisation {optim_method} : {end - start} secondes")
    # CSVsaver(profile_opt.x, circuit)


def optimize():
    circuit = init_circuit_spline()
    profile0 = init_profile(circuit)
    args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla = init_args_optim(circuit)

    print(f"Nombre de points à considérer: {len(profile0)}")

    optim("SLSQP", profile0, contraintes, args, tol, options_slsqp, bounds, circuit)
    optim("COBYLA", profile0, contraintes, args, tol, options_cobyla, bounds, circuit)
    optim("trust-constr", profile0, contraintes, args, tol, options_trust_constr, bounds, circuit)


if __name__ == "__main__":
    optimize()
