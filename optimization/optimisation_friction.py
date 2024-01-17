import random

import numpy as np
import scipy

from circuit.circuit_polynomial import Circuit
from contraintes_friction import ContrainteNorme2Carre, ContrainteNormeInfini, EnergieDepenseParInstantSpatial, \
    PUISSANCE_ACCELERATION_MAXIMALE
from optimization.costFunction import compute_times_with_air_friction, friction_cost_function


def optimize_boost():
    # Options pour l'algorithme d'optimisation
    Options = {
        "maxiter": 150,
        "disp": True,
        "eps": 0.05,
    }

    circuit = Circuit(coeffs=[0.01, -0.2, 1], segment_length=5, starting_x=0, ending_x=30)
    segments_number = circuit.getNumberSegments()
    initial_boost_profile = [PUISSANCE_ACCELERATION_MAXIMALE * random.random() for i in range(segments_number)]

    # Formulation des optimisation : une contrainte sur l'énergie max sur tout le circuit et une contrainte sur la puissance
    # disponible à un endroit du circuit
    args = (circuit,)
    bounds = ((0, PUISSANCE_ACCELERATION_MAXIMALE) for i in range(segments_number))

    contraintes = [
        {"type": "ineq", "fun": ContrainteNorme2Carre, "args": args},
        {
            "type": "ineq",
            "fun": ContrainteNormeInfini,
        },
    ]

    profile_opt = scipy.optimize.minimize(
        friction_cost_function,
        np.array(initial_boost_profile),
        method="SLSQP",
        constraints=contraintes,
        options=Options,
        args=(circuit,),
        bounds=bounds,
    )

    print(f"Initial boost: {initial_boost_profile}")
    print(f"Optimal boost: {profile_opt.x}")
    print(f"Energie par segment: {EnergieDepenseParInstantSpatial(profile_opt.x, circuit)}")
    print(f"Temps par segment: {compute_times_with_air_friction(profile_opt.x, circuit)}")
    print(f"Energie totale du profil optimal : {sum(EnergieDepenseParInstantSpatial(profile_opt.x, circuit))}")
    print(f"Temps total: {sum(compute_times_with_air_friction(profile_opt.x, circuit))}")


if __name__ == "__main__":
    optimize_boost()
