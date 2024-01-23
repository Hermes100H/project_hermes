import functools
import time
from typing import Union, List

import numpy as np
import scipy

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from contraintes import ContrainteNorme2Carre, ContrainteNormeInfini, CarburantDepenseParInstantSpatial, DebitExpulsionSurLeCircuit
from optimization.costFunction import CostFunction, calcTimings
from optimization.csv_saver_optim import print_optim_info
from optimization.data_analysis.iteration_analysis import store_iteration_data_step
from optimization.data_analysis.optimize_verbose_and_display import optim_display_results
from optimization.parcours_spline.init_circuits_spline import init_circuit_spline_150m_172pts, \
    init_circuit_spline_plat_montee, init_circuit_spline_montee_abrupte
from utils.constants import MASS, DEBIT_EXPULSION_MAXIMAL


def init_circuit(block: bool):
    circuit = Circuit(coeffs=[0, 0, 0], segment_length=1, starting_x=0, ending_x=60)
    circuit.plot_circuit(block=block)
    return circuit


def init_profile(circuit: Union[Circuit, CircuitBspline]):
    nbre_segments = circuit.getNumberSegments()
    profile0 = [0 for i in range(int(nbre_segments))]
    for i in range(int(nbre_segments)):
        profile0[i] = DEBIT_EXPULSION_MAXIMAL
    print(
        f"Carburant depense avec le profil initial : {sum(CarburantDepenseParInstantSpatial(profile0, circuit))}"
    )
    print(f"Temps de parcours du profil inital : {CostFunction(profile0, circuit)}")
    print(f"Profil initial de débit d'expulsion:")
    print(profile0)
    print(f"Temps initiaux :")
    print(calcTimings(profile0, circuit))
    print("Carburant depense par instant spatial :")
    print(CarburantDepenseParInstantSpatial(profile0, circuit))
    return profile0


def init_args_optim(circuit):
    nbre_segments = circuit.getNumberSegments()
    args = (circuit,)
    tol = 1e-6
    bounds = ((0, 10) for i in range(nbre_segments))
    contraintes = [
        {"type": "ineq", "fun": ContrainteNorme2Carre, "args": args},
  #      {
   #         "type": "ineq",
    #        "fun": ContrainteNormeInfini,
     #       "args": args
      #  },
    ]

    options_slsqp = {
        "maxiter": 500,
        "disp": True,
        "eps": 0.1,
    }

    options_cobyla = {"rhobeg": 1.0, "disp": True, "maxiter": 100}

    options_trust_constr = {
        "disp": True,
    }
    return args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla


def evaluate_iteration_steps(circuit: Union[Circuit, CircuitBspline], saved_results: List):
    return functools.partial(store_iteration_data_step, circuit=circuit, saved_results=saved_results)


def optim(optim_method, profile0, contraintes, args, tol, option, bounds, circuit):
    start = time.time()
    saved_results = list()
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
            callback=evaluate_iteration_steps(circuit=circuit, saved_results=saved_results)
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
            callback=evaluate_iteration_steps(circuit=circuit, saved_results=saved_results)
        )
    end = time.time()
    print_optim_info(profile_opt, circuit, optim_method)
    print(f"Temps de calcul de l'optimisation {optim_method} : {end - start} secondes")
    optim_display_results(profile_opt, circuit, saved_results)


def optimize():
    circuit = init_circuit_spline_montee_abrupte(False)
    profile0 = init_profile(circuit)
    args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla = init_args_optim(circuit)

    print(f"Nombre de points à considérer: {len(profile0)}")

    optim("SLSQP", profile0, contraintes, args, tol, options_slsqp, bounds, circuit)
    #optim("COBYLA", profile0, contraintes, args, tol, options_cobyla, bounds, circuit)
    #optim("trust-constr", profile0, contraintes, args, tol, options_trust_constr, bounds, circuit)


if __name__ == "__main__":
    optimize()
