import numpy as np
from numpy import poly1d
from circuit.maths_utils import *

def compute_coord(x_position: float, circuit_function: callable) -> vec2:
    return vec2(x_position, circuit_function(x_position))


def generate_initial_circuit() -> poly1d:
    poly_coeffs = [-0.08, 0.02, 0.3, 0.9, -0.6]
    return np.poly1d(poly_coeffs)

