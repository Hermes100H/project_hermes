from circuit.circuit_bspline import CircuitBspline


def init_circuit_spline_150m_172pts(block: bool):
    y = [0, -1.28, 1.78, 0.36, 3.04, 5.27]
    y = [10 * val for val in y]
    x = [0, 4.29, 8.39, 10.11, 11.48, 16.64]
    x = [10 * val for val in x]
    circuit = CircuitBspline(segment_length=2, x=x, y=y)
    circuit.plot_spline(block)
    return circuit


def init_circuit_spline_plat_montee(block: bool):
    x = [0, 3.46, 6.24, 8.79, 11.56, 13.84]
    y = [0, 0, 1.0, 2.9, 3.73, 6.13]
    y = [10 * val for val in y]
    x = [10 * val for val in x]
    circuit = CircuitBspline(segment_length=1, x=x, y=y)
    circuit.plot_spline(block)
    return circuit


def init_circuit_spline_montee_abrupte(block: bool):
    x = [0, 2.93, 5.36, 6.54, 9.31, 14.11]
    y = [0, 1.75, 3.94, 6.66, 8.84, 8.85]
    y = [10 * val for val in y]
    x = [100 * val for val in x]
    circuit = CircuitBspline(segment_length=10, x=x, y=y)
    circuit.plot_spline(block)
    return circuit


if __name__=="__main__":
    init_circuit_spline_montee_abrupte(True)
