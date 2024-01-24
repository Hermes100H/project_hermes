import random
import re
from typing import List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, animation

from optimization.contraintes import CarburantDepenseParInstantSpatial
from optimization.costFunction import CostFunction
from optimization.initialisation import init_circuit_spline_150m_172pts


def save_csv_iteration(saved_results: List):
    list_iteration = [str(saved_results[i][1]) for i in range(len(saved_results))]
    with open("file.txt", "w") as output:
        output.writelines(list_iteration)


def read_txt_data():
    with open('file.txt', 'r') as file1:
        Lines = file1.readlines()
    list_iteration = list()
    val=""
    for line in Lines:
        line_new = re.split("(])", line)
        if ']' in line_new:
            val += line_new[0]
            list_iteration.append(val)
            val = ""
            val += line_new[2]
        else:
            val += line
    list_iteration_2 = [value.replace("[", "").split() for value in list_iteration]
    list_new = list()
    for i in range(len(list_iteration_2)):
        list_new.append(list())
        for j in range(len(list_iteration_2[0])):
            list_new[-1].append(float(list_iteration_2[i][j]))
    return list_new


def extract_DX():
    file = "/home/alhost/CPE_S9/project_hermes/optimization/optim_results/test/circuit1.csv"
    with open(file, "r") as output:
        file_opened = pd.read_csv(output)
    return file_opened["DX"], file_opened["DY"]


def animate(i, DX, DY, axs, circuit, list_cost=[], list_energy=[]):
    axs[1].cla()
    cmap = plt.get_cmap('magma')
    norm = plt.Normalize(min(i), max(i))
    line_colors = cmap(norm(i))
    cost = CostFunction(i, circuit)
    cost = cost if cost < 20 else 20
    list_cost.append(cost)
    energy = sum(CarburantDepenseParInstantSpatial(i, circuit))
    energy = energy if energy < 80 else 80
    list_energy.append(energy)
    axs[0].scatter(DX, DY, color=line_colors)
    axs[1].plot(list_cost, '-yo')
    axs[2].plot(list_energy, '-ro')


if __name__ == "__main__":
    circuit = init_circuit_spline_150m_172pts(False, segment_length=4)
    list_data = read_txt_data()
    DX, DY = extract_DX()
    DX = list(np.cumsum(DX.tolist()))
    DY = list(np.cumsum(DY.tolist()))
    fig, axs = plt.subplots(3)
    anim = animation.FuncAnimation(fig, animate, frames=list_data, interval=100, fargs=(DX, DY, axs, circuit, ))
    fig.suptitle("Evolution du boost sur le circuit en fonction")
    #anim.event_source.stop()
    #anim.save("anim.gif")
    plt.show()
