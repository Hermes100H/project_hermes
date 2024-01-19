import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

from circuit.circuit_polynomial import Circuit
from optimization.costFunction import CostFunction
from utils.constants import TIME_ON_FAILURE


def circuit_to_look_at():
    circuit = Circuit(coeffs=[0, -1/12, 0], starting_x=0, ending_x=20, segment_length=10)
    return circuit


def cost_function_evolution_over_few_arguments():
    circuit = circuit_to_look_at()
    plt.figure(1)
    circuit.plot_circuit(False)
    step = 0.1
    boost_profile_0 = np.arange(0, 10 + step, step)
    boost_profile_1 = np.arange(0, 10 + step, step)
    boost_profile_x, boost_profile_y = np.meshgrid(boost_profile_0, boost_profile_1)
    cost = np.ndarray((boost_profile_x.shape[0], boost_profile_x.shape[1]))
    for i in range(boost_profile_x.shape[0]):
        for j in range(boost_profile_y.shape[1]):
            cost[i][j] = CostFunction([boost_profile_x[i][j], boost_profile_y[i][j]], circuit)
    max_surface = max(cost[cost < TIME_ON_FAILURE-20])
    cost[cost > TIME_ON_FAILURE - 20] = max_surface + 2
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(boost_profile_x, boost_profile_y, cost, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('Première accélération')
    ax.set_ylabel('Seconde accélération')
    ax.set_zlabel('Fonction de coût')
    plt.title('Fonction de coût en fonction des accélérations dans un cas de 2 segments sans frottement')
    plt.show()


if __name__ == "__main__":
    cost_function_evolution_over_few_arguments()
