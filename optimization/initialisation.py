import functools
from typing import Union, List

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from optimization.contraintes import CarburantDepenseParInstantSpatial, ContrainteNorme2Carre
from optimization.costFunction import CostFunction, calcTimings, compute_times_with_air_friction
from optimization.data_analysis.iteration_analysis import store_iteration_data_step, store_iteration_data_step_friction
from utils.constants import DEBIT_EXPULSION_MAXIMAL


def init_circuit(block: bool, segment_length: int):
    circuit = Circuit(coeffs=[0, 1/100, 0], segment_length=segment_length, starting_x=0, ending_x=150)
    circuit.plot_circuit(block=block)
    return circuit


def init_circuit_spline_150m_172pts(block: bool):
    y = [0, -1.28, 1.78, 0.36, 3.04, 5.27]
    y = [10 * val for val in y]
    x = [0, 4.29, 8.39, 10.11, 11.48, 16.64]
    x = [10 * val for val in x]
    circuit = CircuitBspline(segment_length=2, x=x, y=y)
    circuit.plot_spline(block)
    return circuit


def init_circuit_spline_plat_montee_140m(block: bool, segment_length: int):
    x = [0, 3.46, 6.24, 8.79, 11.56, 13.84]
    y = [0, 0, 1.0, 2.9, 3.73, 6.13]
    y = [10 * val for val in y]
    x = [10 * val for val in x]
    circuit = CircuitBspline(segment_length=segment_length, x=x, y=y)
    circuit.plot_spline(block)
    return circuit


def init_circuit_spline_montee_abrupte(block: bool, segment_length: int):
    x = [0, 2.93, 5.36, 6.54, 9.31, 14.11]
    y = [0, 1.75, 3.94, 6.66, 8.84, 8.85]
    y = [10 * val for val in y]
    x = [10 * val for val in x]
    circuit = CircuitBspline(segment_length=segment_length, x=x, y=y)
    circuit.plot_spline(block)
    return circuit


def init_profile(circuit: Union[Circuit, CircuitBspline], friction: bool = False):
    nbre_segments = circuit.getNumberSegments()
    profile0 = [0 for i in range(int(nbre_segments))]
    for i in range(int(nbre_segments)):
        profile0[i] = DEBIT_EXPULSION_MAXIMAL
    print(
        f"Carburant depense avec le profil initial : {sum(CarburantDepenseParInstantSpatial(profile0, circuit, friction))}"
    )
    print(f"Temps de parcours du profil inital : {CostFunction(profile0, circuit, friction=friction)}")
    print(f"Profil initial de débit d'expulsion:")
    print(profile0)
    print(f"Temps initiaux :")
    if friction:
        timings = compute_times_with_air_friction(profile0, circuit)
    else:
        timings = calcTimings(profile0, circuit)
    print(timings)
    print("Carburant depense par instant spatial :")
    print(CarburantDepenseParInstantSpatial(profile0, circuit, friction))
    return profile0


def init_args_optim(circuit):
    nbre_segments = circuit.getNumberSegments()
    args = (circuit,)
    tol = 1e-6
    bounds = ((0, DEBIT_EXPULSION_MAXIMAL) for i in range(nbre_segments))
    contraintes = [
        {"type": "ineq", "fun": ContrainteNorme2Carre, "args": (circuit,)},
    ]

    options_slsqp = {
        "maxiter": 100,
        "disp": True,
        "eps": 0.2,
    }

    options_cobyla = {"rhobeg": 1.0, "disp": True, "maxiter": 100}

    options_trust_constr = {
        "disp": True,
    }
    return args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla


def init_args_optim_friction(circuit):
    nbre_segments = circuit.getNumberSegments()
    args = (circuit,)
    tol = 1e-4
    bounds = ((0, DEBIT_EXPULSION_MAXIMAL) for i in range(nbre_segments))
    contraintes = [
        {"type": "ineq", "fun": ContrainteNorme2Carre, "args": (circuit, True)},
    ]

    options_slsqp = {
        "maxiter": 60,
        "disp": True,
        "eps": 0.1,
    }

    options_cobyla = {"rhobeg": 1.0, "disp": True, "maxiter": 100}

    options_trust_constr = {
        "disp": True,
    }
    return args, tol, bounds, contraintes, options_trust_constr, options_slsqp, options_cobyla


if __name__=="__main__":
    init_circuit_spline_montee_abrupte(True)


def evaluate_iteration_steps(circuit: Union[Circuit, CircuitBspline], saved_results: List):
    return functools.partial(store_iteration_data_step, circuit=circuit, saved_results=saved_results)


def evaluate_iteration_steps_friction(circuit: Union[Circuit, CircuitBspline], saved_results: List):
    return functools.partial(store_iteration_data_step_friction, circuit=circuit, saved_results=saved_results)

