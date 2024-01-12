import numpy as np


def calculSolutions(dy, dx, vk, G, Fp):
    theta = np.arctan(dy / dx)
    solved = True
    roots_x = np.roots([(1 / 2) * (-G * np.cos(theta) * np.sin(theta) + Fp*np.cos(theta)), vk * np.cos(theta), -dx])
    tsol = 0
    try:
        tsol = np.min([root.real for root in roots_x if abs(root.imag) < 1e-5 and root.real > 0])
    except ValueError:
        print("Pas de solution réelle ou solutions temporelles négatives ")
        solved = False
    return vk, tsol, solved


def calculVitesse(tsol, vk, dy, dx, G, Fp):
    theta = np.arctan(dy/dx)
    solved = True
    vitesse_selon_x = tsol * (- G * np.cos(theta) * np.sin(theta) + Fp * np.cos(theta)) + vk * np.cos(theta)
    if vitesse_selon_x < 0.001:
        print(f"Vitesse selon x négative")
        solved = False
    else:
        vk = np.sqrt((tsol * (-G * np.cos(theta) * np.sin(theta) + Fp * np.cos(theta)) + vk * np.cos(theta)) ** 2 + (
                tsol * (- G * (np.sin(theta) ** 2) + Fp * np.sin(theta)) + vk * np.sin(theta)) ** 2)
    return vk, solved
