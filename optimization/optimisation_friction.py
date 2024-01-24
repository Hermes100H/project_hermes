import time

import numpy as np
import scipy

from optimization.costFunction import friction_cost_function
from optimization.csv_saver_optim import print_optim_info, print_optim_info_friction
from optimization.data_analysis.optimize_verbose_and_display import optim_display_results, \
    optim_display_results_friction
from optimization.initialisation import init_circuit_spline_plat_montee_140m, init_profile, init_args_optim, \
    evaluate_iteration_steps_friction, init_args_optim_friction, init_circuit, init_circuit_spline_montee_abrupte


def optimize_boost():
    # Options pour l'algorithme d'optimisation
    Options = {
        "maxiter": 150,
        "disp": True,
        "eps": 0.05,
    }
    circuit = init_circuit(False, segment_length=5)
    profile0 = init_profile(circuit, friction=True)
    #circuit = Circuit(coeffs=[0.01, -0.2, 1], segment_length=5, starting_x=0, ending_x=30)
    #segments_number = circuit.getNumberSegments()
    #initial_boost_profile = [PUISSANCE_ACCELERATION_MAXIMALE * random.random() for i in range(segments_number)]

    args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla = init_args_optim_friction(circuit)
    print(f"Nombre de points à considérer: {len(profile0)}")

    start = time.time()
    saved_results = list()
    profile_opt = scipy.optimize.minimize(
        friction_cost_function,
        np.array(profile0),
        method="COBYLA",
        constraints=contraintes,
        options=options_slsqp,
        args=args,
        bounds=bounds,
        callback=evaluate_iteration_steps_friction(circuit=circuit, saved_results=saved_results),
    )
    end = time.time()
    print_optim_info_friction(profile_opt, circuit, "SLSQP")
    print(f"Temps de calcul de l'optimisation SLSQP : {end - start} secondes")
    csv_file_name = "plat_montee_friction_140_len_3_kg_23"
    csv_file_name = "plan_incline_friction_15pts_kg_30"
    #optim_display_results_friction(profile_opt, circuit, saved_results, csv_file_name)


if __name__ == "__main__":
    optimize_boost()
