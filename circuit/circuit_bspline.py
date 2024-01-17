import matplotlib.pyplot as plt
import numpy as np
import scipy


class CircuitBspline:
    def __init__(self, x=None, y=None, dx_length=0.1):
        # Solve mutable argument problem
        if y is None:
            y = [1, 3, 3, 0, 2, 1, 4]
        if x is None:
            x = [0, 1 / 2, 3 / 2, 5 / 2, 7 / 2, 9 / 2, 5]
        self.x = x
        self.y = y
        self.start_x = x[0]
        self.end_x = x[-1]
        self.spline = scipy.interpolate.CubicSpline(x, y)
        self.dx_length = dx_length
        self.__circuitCoords = self.discretize()

    def plot_spline(self):
        xs = np.arange(self.start_x, self.end_x + self.dx_length, self.dx_length)
        plt.figure()
        plt.title("Splines")
        plt.plot(self.x, self.y, "go")
        plt.plot(xs, self.spline(xs), "-b")
        plt.show()

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
        spline_x = np.arange(self.start_x, self.end_x + self.dx_length, self.dx_length)
        spline_y = self.spline(spline_x)
        return np.array([spline_x, spline_y]).T

    def GetCircuitCoords(self):
        return self.__circuitCoords
