import numpy as np
import scipy.integrate as itg

class circuit:

    def __init__(self, coeffs=[1,0,0], starting_x = -2, ending_x = 3, segment_length = 0.03):
        self.coeffs = coeffs
        self.start_x = starting_x
        self.end_x = ending_x
        self.segment_length = segment_length
        self.__circuitGenerator = np.poly1d(coeffs)
        self.__circuitCoords = self.discretize(starting_x, ending_x, segment_length)

    def GetDeltas(self):
        coords = self.__circuitCoords
        n = coords.shape[0]
        DX = np.zeros(n-1)
        DY = np.zeros(n-1)
        for i in range(n-1):
            DX[i] = coords[i+1, 0] - coords[i, 0]
            DY[i] = coords[i+1, 1] - coords[i, 1]
        return DX, DY

    def compute_poly_length(self, a: float, b: float) -> float:
        assert a <= b, "a must be lesser than b when computing distance between a and b"

        def df_dx(x):
            return np.sqrt(1 + self.__circuitGenerator.deriv()(x) ** 2)

        return itg.quad(df_dx, a, b)[0]
    
    def find_next_x(self, x, threshold, segment_length):
        x_next_inf = x
        x_next_max = x + 10
        while True:
            x_mid = (x_next_max+x_next_inf)/2.0
            error = self.compute_poly_length(x, x_mid) - segment_length
            if abs(error) < threshold:
                return x_mid
            if error>0:
                x_next_max = x_mid
            else:
                x_next_inf = x_mid

    def discretize(self, starting_x=-3, ending_x=2.8, segment_length=0.03):
        X = []
        Y = []
        threshold = 1e-10
        x_current = starting_x
        while x_current < ending_x:
            x_current = self.find_next_x(x_current, threshold, segment_length)
            X.append(x_current)
            Y.append(self.__circuitGenerator(x_current))
        return np.array([X,Y]).T
    
    def GetCircuitCoords(self):
        return self.__circuitCoords
    
    def GetCircuitGenerator(self):
        return self.__circuitGenerator