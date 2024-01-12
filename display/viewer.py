import numpy as np
from random import *
from display.constants import *
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation

class viewer:

    def __init__(self, car, circuit, v0=0, energy=20):
        # Parameters
        self.__car = car
        self.__circuit = circuit
        self.__energy = energy
        self.__v0 = v0

        # Amount of points
        self.__n = self.__circuit.GetCircuitCoords().shape[0]

        # Graphic display
        self.__coords_x = [self.__circuit.GetCircuitCoords()[0,0]]
        self.__coords_y = [self.__circuit.GetCircuitCoords()[0,1]]
        self.__speeds = [v0]
        self.__profile = self.GenerateProfile()
        self.__circuitGeneratorDerivate = self.__circuit.GetCircuitGenerator().deriv()
        self.__interval = 5
        self.__frame_max = 370
        self.__fig, self.__ax = plt.subplots(figsize = (15,10))
        self.__real_line, = self.__ax.plot([], [], label='Trajectoire voiture', marker = '.', markersize = 10)
        self.__time_stop = 0
        self.__compute_time_stop = True


    def GenerateProfile(self):
        count = 0
        ret = np.zeros(self.__n)
        for i in range(self.__n):
            if count < self.__energy:
                r = random()
                if r < 0.4:
                    ret[i] = 1
                    count += 1
        return ret

    def GetDeltas(self):
        coords = self.__circuit.GetCircuitCoords()
        DX = np.zeros(self.__n)
        DY = np.zeros(self.__n)
        for i in range(1, self.__n):
            DX[i] = coords[i,0] - coords[i-1,0]
            DY[i] = coords[i,1] - coords[i-1,1]
        return [DX, DY]

    def ComputeDelta1(self, dx, dy, vk):
        theta = np.arctan(dy/dx)
        ret = (vk * np.cos(theta))** 2 - 2 * dx * g * np.cos(theta) * np.sin(theta)
        return ret

    def ComputeDelta2(self, dx, dy, vk):
        theta = np.arctan(dy/dx)
        ret = (vk * np.sin(theta))**2 - 2 * dy * g * np.sin(theta)**2
        return ret
    
    def ComputeSpeedNorm(self, dx, dy, t, vk):
        theta = np.arctan(dy/dx)
        sign = np.sign(-g * t  + g * t *np.cos(theta)**2 + vk * np.sin(theta))
        ret = np.sqrt((-g*t*np.cos(theta)*np.sin(theta) + vk*np.cos(theta))**2 + (-g*t + g*t*np.cos(theta)**2 + vk*np.sin(theta))**2)
        return ret
    
    def ComputeTimes1(self, dx, dy, vk, delta1):
        theta = np.arctan(dy/dx)
        t1 = (vk * np.cos(theta) + np.sqrt(delta1)) / (g * np.cos(theta) * np.sin(theta))
        t2 = (-vk * np.cos(theta) + np.sqrt(delta1)) / (-g * np.cos(theta) * np.sin(theta))
        return [t1, t2]
    
    def ComputeTimes2(self, dx, dy, vk, delta2):
        theta = np.arctan(dy/dx)
        t3 = (vk * np.sin(theta) + np.sqrt(delta2)) / (g * np.sin(theta)**2)
        t4 = (-vk * np.sin(theta) + np.sqrt(delta2)) / (-g * np.sin(theta)**2)
        return [t3,t4]

    def ComputeAll(self):
        profile = self.GenerateProfile()
        [deltas_x, deltas_y] = self.GetDeltas()
        Tk = []
        vk = self.__v0
        for i in range(1,self.__n):
            dx = deltas_x[i]
            dy = deltas_y[i]
            delta = self.ComputeDelta1(dx, dy, vk)
            [t1, t2] = self.ComputeTimes1(dx, dy, vk, delta)
            if (t1 < 0) or (t2 > 0 and t2 < t1 and t1 > 0):
                t = t2
            else:
                t = t1
            Tk.append(t)
            vk = self.ComputeSpeedNorm(dx, dy, t, vk)
        Tk.append(0)
        self.__times = Tk

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
        
    def Init(self):
        return self.__real_line,

    def Show(self):
        self.__fig.suptitle('Trajectoire')
        coords = self.__circuit.GetCircuitCoords()
        line, = self.__ax.plot(coords[:,0], coords[:,1], label = 'Circuit')
        line.set_color('black')
        animation = FuncAnimation(self.__fig, self.Update, frames = self.__frame_max, blit=True, interval=self.__interval, repeat = True)
        plt.draw()
        plt.show()