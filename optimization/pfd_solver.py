from typing import Tuple

import numpy as np
from sympy import Reals, Symbol, cos, exp, nsolve, sin

from circuit.maths_utils import compute_angle
from utils.constants import CONST_MU, MASS, SPEED_ON_FAILURE, TIME_ON_FAILURE, CONST_g


def calculSolutions(dy, dx, vk, G, Fp):
    theta = np.arctan(dy / dx)
    solved = True
    roots_x = np.roots([(1 / 2) * (-G * np.cos(theta) * np.sin(theta) + Fp * np.cos(theta)), vk * np.cos(theta), -dx])
    tsol = 0
    try:
        tsol = np.min([root.real for root in roots_x if abs(root.imag) < 1e-5 and root.real > 0])
    except ValueError:
        print("Pas de solution réelle ou solutions temporelles négatives ")
        solved = False
    return vk, tsol, solved


def calculVitesse(tsol, vk, dy, dx, G, Fp):
    theta = compute_angle(dy, dx)
    solved = True
    vitesse_selon_x = tsol * (-G * np.cos(theta) * np.sin(theta) + Fp * np.cos(theta)) + vk * np.cos(theta)
    if vitesse_selon_x < 0.001:
        print(f"Vitesse selon x négative")
        solved = False
    else:
        vk = np.sqrt(
            (tsol * (-G * np.cos(theta) * np.sin(theta) + Fp * np.cos(theta)) + vk * np.cos(theta)) ** 2
            + (tsol * (-G * (np.sin(theta) ** 2) + Fp * np.sin(theta)) + vk * np.sin(theta)) ** 2
        )
    return vk, solved


def solve_position_ode_with_air_friction(
    delta_x: float,
    initial_speed: float,
    boost_force: float,
    theta: float,
    friction_coeff: float = CONST_MU,
    mass: float = MASS,
) -> Tuple[float, float]:
    coeff_A = (mass**2 * (boost_force - CONST_g * sin(theta)) - mass * friction_coeff * initial_speed * cos(theta)) / (
        friction_coeff**2 * cos(theta)
    )
    coeff_lambda = mass * (boost_force - CONST_g * sin(theta)) / friction_coeff
    coeff_tau = mass / (friction_coeff * cos(theta))
    t = Symbol("t", positive=True)

    x_t_next = coeff_A * (exp(-t / coeff_tau) - 1) + coeff_lambda * t - delta_x

    initial_guess = 0.2
    try:
        t_next = nsolve(x_t_next, t, initial_guess, domain=Reals, positive=True)
        if t_next < 0:
            raise ValueError
        v_t_next = (-(coeff_A / coeff_tau) * exp(-t_next / coeff_tau) + coeff_lambda) / cos(theta)
    except ValueError:
        t_next = TIME_ON_FAILURE
        v_t_next = SPEED_ON_FAILURE
    return t_next, v_t_next
