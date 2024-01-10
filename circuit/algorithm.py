import numpy as np
from random import *
from constants import *

class algorithm:

    def __init__(self, car, circuit):
        self.__car = car
        self.__circuit = circuit
        self.__n = self.__circuit.GetCircuitCoords().shape[0]
        self.__energy = 20

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

    def ComputeAll(self):
        profile = self.GenerateProfile()
        [deltas_x, deltas_y] = self.GetDeltas()