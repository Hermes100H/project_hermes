import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class viewer:

    def __init__(self, car, circuit, v0=0, energy=20):
        # Parameters
        self.__car = car
        self.__circuit = circuit
        self.__energy = energy

        # Amount of points
        self.__n = self.__circuit.GetCircuitCoords().shape[0]

        # Graphic display
        self.__coords_x = [self.__circuit.GetCircuitCoords()[0,0]]
        self.__coords_y = [self.__circuit.GetCircuitCoords()[0,1]]
        self.__speeds = [v0]
        self.__circuitGeneratorDerivate = self.__circuit.GetCircuitGenerator().deriv()
        self.__interval = 5
        self.__frame_max = 370
        self.__fig, self.__ax = plt.subplots(figsize = (15,10))
        self.__real_line, = self.__ax.plot([], [], label='Trajectoire voiture', marker = '.', markersize = 10)
    
    def ComputeSpeedNorm(self, dx, dy, t, vk):
        theta = np.arctan(dy/dx)
        sign = np.sign(-g * t  + g * t *np.cos(theta)**2 + vk * np.sin(theta))
        ret = np.sqrt((-g*t*np.cos(theta)*np.sin(theta) + vk*np.cos(theta))**2 + (-g*t + g*t*np.cos(theta)**2 + vk*np.sin(theta))**2)
        return ret

    def Update(self, frame):
        xk = self.__coords_x[-1]
        yk = self.__coords_y[-1]
        vk = self.__speeds[-1]
        theta = np.arctan(self.__circuitGeneratorDerivate(xk))
        t = self.__interval / 1000
        x = - g/2 * np.cos(theta) * np.sin(theta) * t**2 + vk * np.cos(theta) * t + xk
        y = g/2 * np.cos(theta)**2 * t ** 2 - g/2 * t ** 2 + vk * t * np.sin(theta) + yk
        dx = x-xk
        dy = y-yk
        v = self.ComputeSpeedNorm(dx, dy, t, vk)
        self.__coords_x.append(x)
        self.__coords_y.append(y)
        self.__speeds.append(v)
        self.__real_line.set_data(self.__coords_x[-1], self.__coords_y[-1])
        if vk < 0 :
            self.__real_line.set_color('r')
        else :
            self.__real_line.set_color('b')
        return self.__real_line,

    def Show(self):
        self.__fig.suptitle('Trajectoire')
        coords = self.__circuit.GetCircuitCoords()
        line, = self.__ax.plot(coords[:,0], coords[:,1], label = 'Circuit')
        line.set_color('black')
        animation = FuncAnimation(self.__fig, self.Update, frames = self.__frame_max, blit=True, interval=self.__interval, repeat = True)
        plt.draw()
        plt.show()