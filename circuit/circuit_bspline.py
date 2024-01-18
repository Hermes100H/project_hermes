import matplotlib.pyplot as plt
import numpy as np
import scipy


from circuit.maths_utils import compute_poly_length_spline


class CircuitBspline:

    def __init__(self, x=None, y=None, segment_length=0.1):
        # Solve mutable argument problem
        if y is None:
            y = [0, 2, 2, -1, 1, 0, 3]
        if x is None:
            x = [0, 1 / 2, 3 / 2, 5 / 2, 7 / 2, 9 / 2, 5]
        self.x = x
        self.y = y
        self.start_x = x[0]
        self.end_x = x[-1]
        self.spline = scipy.interpolate.CubicSpline(x, y)
        self.segment_length = segment_length
        self.__circuitCoords = self.discretize()

    def plot_spline(self):
        xs = np.arange(self.start_x, self.end_x + 0.1, 0.1)
        plt.figure()
        plt.title("Splines")
        plt.plot(self.x, self.y, "go")
        plt.plot(xs, self.spline(xs), "-b")
        plt.show()

    def get_spline_point_tangent(self):
        for xi in self.x:
            print(self.spline.derivative()(xi))

    def GetDeltas(self):
        coords = self.__circuitCoords
        n = coords.shape[0]
        DX = np.zeros(n - 1)
        DY = np.zeros(n - 1)
        for i in range(n - 1):
            DX[i] = coords[i + 1, 0] - coords[i, 0]
            DY[i] = coords[i + 1, 1] - coords[i, 1]
        return DX, DY

    def discretize(self) -> np.array:
        spline_x = []
        spline_y = []
        threshold = 1e-10
        x_current = self.start_x

        def find_next_x(x):
            x_next_inf = x
            x_next_max = x + 100
            while True:
                x_mid = (x_next_max + x_next_inf) / 2.0
                error = compute_poly_length_spline(self.spline, x, x_mid) - self.segment_length
                if abs(error) < threshold:
                    return x_mid
                if error > 0:
                    x_next_max = x_mid
                else:
                    x_next_inf = x_mid

        while x_current < self.end_x:
            x_current = find_next_x(x_current)
            spline_x.append(x_current)
            spline_y.append(self.spline(x_current))
        return np.array([spline_x, spline_y]).T

    def GetCircuitCoords(self):
        return self.__circuitCoords

    def getNumberSegments(self):
        return self.__circuitCoords.shape[0] - 1
