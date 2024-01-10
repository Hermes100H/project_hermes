from generate_circuit import *
from maths_utils import *
from constants import *
import matplotlib.pyplot as plt
from car import *
import matplotlib.animation as animation

circuit_generator = generate_initial_circuit()

s = np.zeros([n,2])
for i in range(n):
    q = i
    s[i,0] = q
    s[i,1] = circuit_generator(q)

my_car = car(vec2(s[0,0],s[0,1]), vec2(0.1,0.1))

# plt.plot(s[:,1])
# plt.plot(my_car.GetPos().x, my_car.GetPos().y, marker="o", markersize=10, markerfacecolor="red")
# plt.show()

# tentative 
fig, ax = plt.subplots()
s_x = s[:,0]
s_z = s[:,1]

scat = ax.scatter(s_x[0], s_z[0],c = 'b',  label = "Circuit")
line_2 = ax.plot(s_x[0], s_z[0], label = "Voiture", marker = "o", markersize=10, markerfacecolor="red")[0]
ax.set(xlim = [0,1000], ylim = [0,1])
ax.legend()

def update(frame):
    x = s_x[:frame]
    y = s_z[:frame]
    data = np.stack([x,y]).T
    scat.set_offsets(data)
    line_2.set_xdata(s_x[:frame])
    line_2.set_ydata(s_z[:frame])
    return (scat,line_2)
    
ani = animation.FuncAnimation(fig = fig, func = update, frames= n, interval = 100)
plt.show()

print(s_x)