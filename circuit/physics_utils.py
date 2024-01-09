g = 9.81
MAX_SPEED = 55


def compute_height_potential_energy(z: float, m: float, z_0=0) -> float:
    return m * g * (z-z_0)


def compute_kinematic_energy(speed: float, m: float) -> float:
    return 0.5 * m * speed ** 2


def compute_total_energy(height, mass, speed, z_0=0) -> float:
    return compute_height_potential_energy(height, mass, z_0) + compute_kinematic_energy(speed, mass)


def compute_gravity_force(mass: float) -> float:
    return mass * g


def compute_friction_force(speed: float, friction_coeff: float) -> float:
    interpolation_coeff = speed / MAX_SPEED
    linear_friction = -friction_coeff * speed
    quadratic_friction = -friction_coeff * speed ** 2
    return (1 - interpolation_coeff) * linear_friction + interpolation_coeff * quadratic_friction
