import numpy as np
import scipy.integrate as itg

class circuit:

    def __init__(self, coeffs=[-0.08, -0.02, 0.3, 0.9, -0.6]):
        self.__circuitGenerator = np.poly1d(coeffs)
        self.__circuitCoords = self.discretize(starting_x=-2, ending_x= 3)


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