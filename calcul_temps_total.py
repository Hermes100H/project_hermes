import numpy as np
from matplotlib import pyplot as plt

from ResolutionSystemePFD import calculSolutions, calculVitesse

Temps_total = 0

list_t = list()


def calcTimingForDisplay(plist_x, plist_v, profile):
    t = 0
    vk = 0
    G = 10
    dx = 1
    dy = 1/12
    VITESSE_SUPP = 10
    index_profile = 0
    plist_v.append(vk)
    for val in plist_x:
        Force_poussee = profile[index_profile] * VITESSE_SUPP
        vk, tsol, solved_solution = calculSolutions(dy, dx, vk, G, Force_poussee)
        vk, solved_vitesse = calculVitesse(tsol, vk, dy, dx, G, Force_poussee)
        if not solved_solution or not solved_vitesse:
            t += 10000
            break
        list_t.append(tsol)
        plist_v.append(vk)
        t += tsol
        index_profile += 1
    return t


nbre_segments = 10

profile = [0 for i in range(nbre_segments)]
for i in range(3):
    profile[i] = 1
list_x = [i for i in range(nbre_segments)]
list_v = []

print(f"{calcTimingForDisplay(list_x, list_v, profile)} secondes")

array_x = np.array(list_x)
array_v = np.array(list_v)

plt.figure(1)
plt.plot(array_v)
plt.title("Vitesse en fonction de la position sur la courbe")
plt.xlabel("Position sur la droite")
plt.ylabel("Vitesse")
plt.show()

plt.figure(2)
plt.plot(list_t)
plt.title("Temps solution du PFD")
plt.ylabel("Temps")
plt.legend(["t"])
plt.show()
