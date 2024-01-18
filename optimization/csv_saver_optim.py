import csv
import os
from datetime import datetime
from typing import Union

from scipy.optimize import OptimizeResult

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from optimization.contraintes import EnergieDepenseParInstantSpatial
from optimization.costFunction import calcTimings


def CSVsaver(optim_result_profile, circuit: Union[Circuit, CircuitBspline], file_name: str):
    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    try:
        os.makedirs("./optim_results/test")
    except FileExistsError:
        pass
    with open(
        f"./optim_results/test/circuit_{file_name}.csv",
        "w",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["profile", "timing", "energy", "DX", "DY"])
        dx, dy = circuit.GetDeltas()
        columns = [
            tuple(optim_result_profile),
            tuple(calcTimings(optim_result_profile, circuit)),
            tuple(EnergieDepenseParInstantSpatial(optim_result_profile, circuit)),
            tuple(dx),
            tuple(dy),
        ]
        rows = zip(*columns)
        writer.writerows(rows)


def print_optim_info(boost_profile_optimal: OptimizeResult, circuit: Circuit, optim_method: str):
    print("===================================================")
    print(f"\n\nOptimisation avec {optim_method}")
    print("Profil de boost obtenu :")
    print(boost_profile_optimal.x)
    print(f"Temps de parcours, méthode {optim_method} : {boost_profile_optimal.fun} secondes")
    print("Profil d'énergie obtenu : ")
    print(EnergieDepenseParInstantSpatial(boost_profile_optimal.x, circuit))
    print("Temps à chaque instant spatial :")
    print(calcTimings(boost_profile_optimal.x, circuit))
    print(
        f"Energie totale du profil optimal : {sum(EnergieDepenseParInstantSpatial(boost_profile_optimal.x, circuit))}"
    )
