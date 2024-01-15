from circuit.generate_circuit import *
from circuit.maths_utils import *
from car.car import *
from circuit.circuit import Circuit
from display.viewer import *

circuit_generator = generate_initial_circuit()

s = np.zeros([n,2])
for i in range(n):
    q = i
    s[i,0] = q
    s[i,1] = circuit_generator(q)

my_car = car(Vec2(s[0,0], s[0,1]), Vec2(0.1, 0.1))

c = Circuit([1, 0, 0])
coords = c.GetCircuitCoords()
test = np.arange(0,1.2,0.1)

algo = viewer(my_car, c, 0)
algo.Show()