import numpy as np
import matplotlib.pyplot as plt

from circuit.maths_utils import compute_poly_length


class Circuit:
    def __init__(self, coeffs=[1, 0, 0], starting_x=-2, ending_x=3, segment_length=0.03):
        self.coeffs = coeffs
        self.start_x = starting_x
        self.end_x = ending_x
        self.segment_length = segment_length
        self.__circuit = np.poly1d(coeffs)
        self.__circuitCoords = self.discretize(starting_x, ending_x, segment_length)

    def plot_circuit(self, block: bool):
        plt.plot(self.__circuitCoords[:, 0], self.__circuitCoords[:, 1])
        plt.show(block=block)

    def GetDeltas(self):
        coords = self.__circuitCoords
        n = coords.shape[0]
        DX = np.zeros(n - 1)
        DY = np.zeros(n - 1)
        for i in range(n - 1):
            DX[i] = coords[i + 1, 0] - coords[i, 0]
            DY[i] = coords[i + 1, 1] - coords[i, 1]
        return DX, DY

    def discretize(self, starting_x: float, ending_x: float, segment_length: float = 0.1) -> np.array:
        X = []
        Y = []
        threshold = 1e-10
        x_current = starting_x

        def find_next_x(x):
            x_next_inf = x
            x_next_max = x + 100
            while True:
                x_mid = (x_next_max + x_next_inf) / 2.0
                error = compute_poly_length(self.__circuit, x, x_mid) - segment_length
                if abs(error) < threshold:
                    return x_mid
                if error > 0:
                    x_next_max = x_mid
                else:
                    x_next_inf = x_mid

        while x_current < ending_x:
            x_current = find_next_x(x_current)
            X.append(x_current)
            Y.append(self.__circuit(x_current))
        return np.array([X, Y]).T

    def GetCircuitCoords(self):
        return self.__circuitCoords

    def GetCircuitGenerator(self):
        return self.__circuit

    def getNumberSegments(self):
        return self.__circuitCoords.shape[0] - 1


if __name__ == "__main__":
    c = Circuit()
    c.plot_circuit(True)
