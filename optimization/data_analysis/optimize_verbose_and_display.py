from typing import Union, List

from scipy.optimize import OptimizeResult

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from display.display_acceleration_function import plot_boost_profile
from optimization.csv_saver_optim import CSVsaver, CSVsaverFriction
from optimization.data_analysis.iteration_analysis import plot_iteration_steps
from optimization.data_analysis.profile_iteration_behavior import save_csv_iteration


def optim_display_results(profile_opt: OptimizeResult, circuit: Union[Circuit, CircuitBspline], saved_results: List, file_name: str):
    folder = CSVsaver(profile_opt.x, circuit, file_name=file_name)
    plot_boost_profile(file_name + ".csv", csv_folder=folder)
    plot_iteration_steps(saved_results=saved_results, block=True)
    save_csv_iteration(saved_results)


def optim_display_results_friction(profile_opt: OptimizeResult, circuit: Union[Circuit, CircuitBspline], saved_results: List, file_name: str):
    csv_folder = CSVsaverFriction(profile_opt.x, circuit, file_name=file_name)
    plot_boost_profile(file_name + ".csv", csv_folder)
    plot_iteration_steps(saved_results=saved_results, block=True)
