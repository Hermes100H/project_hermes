import csv
import os
from datetime import datetime
from typing import Union

from scipy.optimize import OptimizeResult

from circuit.circuit_bspline import CircuitBspline
from circuit.circuit_polynomial import Circuit
from optimization.contraintes import CarburantDepenseParInstantSpatial, DebitExpulsionSurLeCircuit
from optimization.costFunction import calcTimings


def CSVsaver(optim_result_profile, circuit: Union[Circuit, CircuitBspline], file_name: str):
    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    folder = "./optim_results/test/"
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass
    with open(
        f"{folder}{file_name}.csv",
        "w+",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["profile", "timing", "energy", "DX", "DY"])
        dx, dy = circuit.GetDeltas()
        columns = [
            tuple(optim_result_profile),
            tuple(calcTimings(optim_result_profile, circuit)),
            tuple(CarburantDepenseParInstantSpatial(optim_result_profile, circuit)),
            tuple(dx),
            tuple(dy),
        ]
        rows = zip(*columns)
        writer.writerows(rows)
    return folder


def print_optim_info(boost_profile_optimal: OptimizeResult, circuit: Circuit, optim_method: str):
    print("===================================================")
    print(f"\n\nOptimisation avec {optim_method}")
    print("Profil de débit d'expulsion obtenu :")
    print(boost_profile_optimal.x)
    print(f"Temps de parcours, méthode {optim_method} : {boost_profile_optimal.fun} secondes")
    print("Profil d'énergie obtenu : ")
    print(CarburantDepenseParInstantSpatial(boost_profile_optimal.x, circuit))
    print("Temps à chaque instant spatial :")
    print(calcTimings(boost_profile_optimal.x, circuit))
    print(
        f"Carburant total dépensé du profil optimal : {sum(CarburantDepenseParInstantSpatial(boost_profile_optimal.x, circuit))}"
    )
    print("Debit par instant sur le circuit")
    print(DebitExpulsionSurLeCircuit(boost_profile_optimal.x, circuit))


def CSVsaverFriction(optim_result_profile, circuit: Union[Circuit, CircuitBspline], file_name: str):
    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    folder = "./optim_results/test/"
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass
    with open(
        f"{folder}{file_name}.csv",
        "w+",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["profile", "timing", "energy", "DX", "DY"])
        dx, dy = circuit.GetDeltas()
        columns = [
            tuple(optim_result_profile),
            tuple(calcTimings(optim_result_profile, circuit, friction=True)),
            tuple(CarburantDepenseParInstantSpatial(optim_result_profile, circuit, friction=True)),
            tuple(dx),
            tuple(dy),
        ]
        rows = zip(*columns)
        writer.writerows(rows)
    return folder


def print_optim_info_friction(boost_profile_optimal: OptimizeResult, circuit: Circuit, optim_method: str):
    print("===================================================")
    print(f"\n\nOptimisation avec {optim_method}")
    print(f"Temps de parcours, méthode {optim_method} : {boost_profile_optimal.fun} secondes")
    print("Profil d'énergie obtenu : ")
    print(CarburantDepenseParInstantSpatial(boost_profile_optimal.x, circuit, friction=True))
    print("Temps à chaque instant spatial :")
    print(calcTimings(boost_profile_optimal.x, circuit, friction=True))
    print(
        f"Carburant total dépensé du profil optimal : {sum(CarburantDepenseParInstantSpatial(boost_profile_optimal.x, circuit, friction=True))}"
    )
    print("Profil de débit d'expulsion obtenu :")
    print(boost_profile_optimal.x)
