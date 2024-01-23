import numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_boost_profile(file_name):
    csv_folder = "/home/arthur.l-host/Documents/S9/projet_hermes/project_hermes/optimization/optim_results/test/"
    data = pd.read_csv(csv_folder+file_name)
    acceleration_boost = data["profile"].to_numpy()
    acceleration_boost = numpy.concatenate((acceleration_boost, np.array((0,)))).tolist()
    dx = data["DX"].to_numpy()
    dx_cumul = numpy.concatenate((np.array((0,)), dx)).tolist()
    for i in range(len(dx_cumul)-1):
        dx_cumul[i+1] = dx_cumul[i] + dx[i]
    plt.figure()
    plt.plot(dx_cumul, acceleration_boost)
    plt.title("Debit en fonction de la position")
    plt.xlabel("Position")
    plt.ylabel("Force fournie")
    plt.show(block=False)
    

if __name__ == "__main__":
    file = "spline1901_150m_172pts.csv"
    plot_boost_profile(file)
