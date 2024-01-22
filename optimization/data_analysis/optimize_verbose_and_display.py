from typing import Union, List

from scipy.optimize import OptimizeResult

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from display.display_acceleration_function import plot_boost_profile
from optimization.csv_saver_optim import CSVsaver
from optimization.data_analysis.iteration_analysis import plot_iteration_steps


def optim_display_results(profile_opt: OptimizeResult, circuit: Union[Circuit, CircuitBspline], saved_results: List):
    file_name = "SplineCubiqueUnity_pluslong_test"
    CSVsaver(profile_opt.x, circuit, file_name=file_name)
    plot_boost_profile(file_name + ".csv")
    plot_iteration_steps(saved_results=saved_results, block=True)
