import numpy as np
from matplotlib import pyplot as plt

Temps_total = 0
G = 10
dx = 1
dy = -1/3
theta = np.arctan(dy/dx)
list_t1 = list()
list_t2 = list()
list_t3 = list()
list_t4 = list()


def calcTiming(plist_x, plist_v):
    t = 0
    vk = 0
    for val in plist_x:
        delta_x = (vk * np.cos(theta)) ** 2 - 2 * dx * G * np.cos(theta) * np.sin(theta)
        delta_y = (vk * np.sin(theta)) ** 2 - 2 * dy * G * (np.sin(theta) ** 2)
        t1 = (vk*np.cos(theta) + np.sqrt(delta_x))/(G*np.cos(theta)*np.sin(theta))
        t2 = (-vk*np.cos(theta) + np.sqrt(delta_x))/(-G*np.cos(theta)*np.sin(theta))
        t3 = (vk*np.sin(theta) + np.sqrt(delta_y))/(G*(np.sin(theta)**2))
        t4 = (-vk*np.sin(theta) + np.sqrt(delta_y))/(-G*(np.sin(theta)**2))
        if (abs(t2 - t3) <= 0.001 or abs(t2 - t4) <= 0.001) and t2 > 0:
            tsol = t2
        else:
            tsol = t1
        list_t1.append(t1)
        list_t2.append(t2)
        list_t3.append(t3)
        list_t4.append(t4)
        vk = np.sqrt((G ** 2) * (np.sin(theta)**2) * tsol - 2 * G * tsol * (np.cos(theta)**2 * np.sin(theta) + np.sin(theta) ** 2) + vk**2)
        plist_v.append(vk)
        t += tsol
    return t


list_x = [i for i in range(20)]
list_v = []

calcTiming(list_x, list_v)

array_x = np.array(list_x)
array_v = np.array(list_v)

plt.plot(array_x, array_v)
plt.title("Vitesse en fonction de la position sur la courbe")
plt.xlabel("Position sur la droite")
plt.ylabel("Vitesse")
plt.show()
