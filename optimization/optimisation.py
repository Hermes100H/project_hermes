import time

import numpy as np
import scipy

from optimization.costFunction import CostFunction
from optimization.csv_saver_optim import print_optim_info
from optimization.data_analysis.optimize_verbose_and_display import optim_display_results
from optimization.initialisation import init_profile, init_args_optim, init_circuit_spline_montee_abrupte, \
    evaluate_iteration_steps, init_circuit_spline_plat_montee_140m


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
    file_name_csv = "plat_montee_140m_segment_length_4_10_kg"
    optim_display_results(profile_opt, circuit, saved_results, file_name=file_name_csv)


def optimize():
    circuit = init_circuit_spline_plat_montee_140m(False, segment_length=4)
    profile0 = init_profile(circuit)
    args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla = init_args_optim(circuit)

    print(f"Nombre de points à considérer: {len(profile0)}")

    optim("SLSQP", profile0, contraintes, args, tol, options_slsqp, bounds, circuit)
    #optim("COBYLA", profile0, contraintes, args, tol, options_cobyla, bounds, circuit)
    #optim("trust-constr", profile0, contraintes, args, tol, options_trust_constr, bounds, circuit)


if __name__ == "__main__":
    optimize()
