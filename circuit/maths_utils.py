import numpy as np
import scipy.integrate as itg
from math import comb
from numpy import poly1d


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def compute_poly_length(poly_function: np.poly1d, a: float, b: float) -> float:
    assert a <= b, "a must be lesser than b when computing distance between a and b"

    def df_dx(x):
        return np.sqrt(1 + poly_function.deriv()(x) ** 2)

    return itg.quad(df_dx, a, b)[0]


def bezier_function(*control_points: Vec2):
    B_x = np.poly1d([0])
    B_y = np.poly1d([0])
    N = len(control_points) - 1
    for i, control_point in enumerate(control_points):
        coeff_x = comb(N, i) * control_point.x
        coeff_y = comb(N, i) * control_point.y
        B_right = poly1d([1] + [0 for k in range(i)])
        B_left = poly1d([1 for k in range(N - i)], r=True)
        B = B_left * B_right
        print("----------")
        print(B_left)
        print(B_right)
        B_x += coeff_x * B
        B_y += coeff_y * B
    return B_x, B_y


def compute_angle(dy: float, dx: float):
    return np.arctan(dy / dx)

