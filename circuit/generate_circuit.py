import time
from typing import List
import numpy as np
from numpy import poly1d

from matplotlib import pyplot as plt

from circuit.maths_utils import vec2, compute_poly_length


def compute_coord(x_position: float, circuit_function: callable) -> vec2:
    return vec2(x_position, circuit_function(x_position))


def generate_initial_circuit(poly_coeffs=[-0.08, 0.02, 0.3, 0.9, -0.6]) -> poly1d:
    return np.poly1d(poly_coeffs)

def discretize_circuit(circuit: poly1d, starting_x=0, ending_x=1, dx=0.001) -> List[float]:

    i=0
    x_current = starting_x
    x_following = 0
    x_coords = [x_current]
    y_coords = [circuit(x_current)]

    while x_current < ending_x:
        print(i)

        y_following = circuit(x_current) + dx*circuit.deriv()(x_current)
        y_coords.append(y_following)

        xs_following_solutions = (circuit - y_following).roots

        #xs_candidates = xs_following_solutions.real[abs(xs_following_solutions.imag) < 1e-2]
       # xs_candidates = xs_candidates > x_current

        xs_candidates = [x.real for x in xs_following_solutions if abs(x.imag) < 1e-1 and x.real > x_current]
        x_following = min(xs_candidates)

        x_coords.append(x_following)
        x_current = x_following
        i+=1

    return x_coords, y_coords




def d_circuit(circuit: poly1d, starting_x=0, ending_x=1, semgent_length=0.2):

    X = []
    threshold = 1e-10

    def find_next_x(x):
        x_next_inf = x
        x_next_max = x + 10
        while True:
            x_mid = (x_next_max+x_next_inf)/2.0
            error = compute_poly_length(circuit, x, x_mid) - semgent_length
            if abs(error) < threshold:
                return x_mid
            if error>0:
                x_next_max = x_mid
            else:
                x_next_inf = x_mid


    x_current = starting_x
    while x_current < ending_x:
        print(f'Working for {x_current}')
        x_current = find_next_x(x_current)
        X.append(x_current)

    return X



if __name__ == "__main__":

    circuit = generate_initial_circuit([1,1,0])

    start = time.time()
    X = d_circuit(circuit, 1, 3, 0.1)
    test = np.arange(1,3,0.1)
    plt.plot(X, circuit(X), 'r+', test, circuit(test))
    plt.show()

    print(time.time() - start)




