from typing import List

from circuit.circuit import Circuit
from circuit.maths_utils import compute_angle
from optimization.pfd_solver import calculSolutions, calculVitesse, solve_position_ode_with_air_friction
from utils.constants import INITIAL_SPEED, TIME_ON_FAILURE, CONST_g


def calcTimings(profile: List, circui: Circuit):
    vk = 0
    dx, dy = circui.GetDeltas()
    timings = list()
    for i in range(dy.shape[0]):
        acceleration = profile[i]
        vk, tsol, solved_solution = calculSolutions(dy[i], dx[i], vk, CONST_g, acceleration)
        vk, solved_vitesse = calculVitesse(tsol, vk, dy[i], dx[i], CONST_g, acceleration)
        if not solved_solution or not solved_vitesse:
            t = 100000
            timings.append(t)
            break
        timings.append(tsol)
    return timings


def compute_times_with_air_friction(boost_profile: List, circuit: Circuit):
    times_per_segments = []
    initial_speed = INITIAL_SPEED
    dx_list, dy_list = circuit.GetDeltas()
    for i in range(dx_list.size):
        dx = dx_list[i]
        dy = dy_list[i]
        boost_force = boost_profile[i]
        theta = compute_angle(dy, dx)
        current_segment_time, initial_speed = solve_position_ode_with_air_friction(
            delta_x=dx, initial_speed=initial_speed, boost_force=boost_force, theta=theta
        )

        times_per_segments.append(current_segment_time)
        if current_segment_time == TIME_ON_FAILURE:
            print("could not find any t to reach next segment")
            break
    return times_per_segments


def CostFunction(profile: List, circui: Circuit):
    return sum(compute_times_with_air_friction(profile, circui))
