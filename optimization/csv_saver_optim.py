import csv
import os
from datetime import datetime

from circuit.circuit import Circuit
from optimization.contraintes import EnergieDepenseParInstantSpatial
from optimization.costFunction import calcTimings


def CSVsaver(optim_result_profile, circui: Circuit):
    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    try:
        os.makedirs("../optim_results/test")
    except FileExistsError:
        pass
    with open(f'../optim_results/test/circuit_{date}_coeffs_{circui.coeffs[0]}_{circui.coeffs[1]}_{circui.coeffs[2]}_start_{circui.start_x}_end_{circui.end_x}_len_{circui.segment_length}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['profile', 'timing', 'energy'])
        columns = [tuple(optim_result_profile), tuple(calcTimings(optim_result_profile, circui)), tuple(EnergieDepenseParInstantSpatial(optim_result_profile, circui))]
        rows = zip(*columns)
        writer.writerows(rows)
