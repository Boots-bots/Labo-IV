import numpy as np
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime

N = 4

# Para chequear cantidad



# Leer y ordenar archivos
if N == 1:
    folder = ("C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PSO1(5_3)/")
    n_gen, n_part = 5, 3
    mejork = (14.48,26.74,9.11)
if N == 2:
    folder = ("C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PSO2(10_5)/" )
    n_gen, n_part = 10, 5
    mejork = (17.72,21.1,14.14)
if N == 3:
    folder = ("C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PSO3(5_3)/")
    n_gen, n_part = 5 , 3 
    mejork = (14.48,26.74,9.11)
if N == 4:
    folder = ("C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/Dia3/ITAE/itae2_n/")
    n_gen, n_part = 5 , 3 
    mejork = (4.99,4.52,2.47)


total = n_gen * n_part

filenames = [f for f in os.listdir(folder) if f.startswith("Kp")]
filenames = sorted(filenames, key=lambda name: re.search(r"_(\d{8})_(\d{6})", name).group(0))
assert len(filenames) == total, f"Se esperaban {total} archivos, pero hay {len(filenames)}"

kp, ki, kd, ise = [[] for _ in range(n_part)], [[] for _ in range(n_part)], [[] for _ in range(n_part)], [[] for _ in range(n_part)]

# Extraer y asignar a cada partícula
for i, name in enumerate(filenames):
    match = re.search(r"Kp(?P<kp>[\d.]+)_Ki(?P<ki>[\d.]+)_Kd(?P<kd>[\d.]+)_Set(?P<set>\d+)_ITAE(?P<ITAE>[\d.]+)", name)
    if match:
        p_idx = i % n_part  # índice de partícula
        kp[p_idx].append(float(match.group("kp")))
        ki[p_idx].append(float(match.group("ki")))
        kd[p_idx].append(float(match.group("kd")))
        ise[p_idx].append(float(match.group("ITAE")))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(n_part):
    ax.plot(kp[i], ki[i], kd[i], '.-', linewidth=1, alpha = 0.5, label=f'P{i+1}')
    ax.scatter(kp[i][-1], ki[i][-1], kd[i][-1], marker='o', s=50, edgecolors='black', facecolors='none')
# ax.scatter(*mejork, marker='*', s=100, color='red' if N == 1 else 'orange', label=f'Mejor Kp-Ki-Kd PSO{N}')
ax.set_xlabel('kp')
ax.set_ylabel('ki')
ax.set_zlabel('kd')
plt.legend()
plt.title('PSO1 - Ks')

plt.figure()
gens = list(range(n_gen))
for i in range(n_part):
    plt.plot(gens, ise[i], '.-', label=f'P{i+1}')
# plt.axhline(mejorise, linestyle='--', color='red' if N == 1 else 'orange', label=f'Mejor ISE PSO{N}')
plt.xlabel('Generación')
plt.ylabel('ITAE')
plt.title('ITAE por partícula')
plt.legend()
plt.grid(True)

plt.show(block=True)


##########################################

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

# Cantidad de partículas y generaciones
n_part = len(kp)
n_gen = len(kp[0])
n_interp = 20  # frames suaves entre generaciones
n_frames = (n_gen - 1) * n_interp + 1

# Preinterpolación: genera kp_smooth[i] con valores interpolados entre generaciones
def interpolate_list(data):
    interp = []
    for i in range(len(data)-1):
        interp += list(np.linspace(data[i], data[i+1], n_interp, endpoint=False))
    interp.append(data[-1])  # agregar el último valor exacto
    return interp

kp_smooth = [interpolate_list(kp[i]) for i in range(n_part)]
ki_smooth = [interpolate_list(ki[i]) for i in range(n_part)]
kd_smooth = [interpolate_list(kd[i]) for i in range(n_part)]

# === ANIMACIÓN ===
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Límites del gráfico
ax.set_xlim(min(map(min, kp)), max(map(max, kp)))
ax.set_ylim(min(map(min, ki)), max(map(max, ki)))
ax.set_zlim(min(map(min, kd)), max(map(max, kd)))

ax.set_xlabel('Kp')
ax.set_ylabel('Ki')
ax.set_zlabel('Kd')
plt.title("Evolución de partículas - PSO")

colors = ['r', 'g', 'b', 'c', 'm', 'y']

# Inicializar líneas y puntos
lines = []
points = []

for i in range(n_part):
    line, = ax.plot([], [], [], '-', color=colors[i % len(colors)], alpha=0.3)
    point = ax.plot([], [], [], 'o', color=colors[i % len(colors)],
                    markersize=4)[0]  # punto más chico
    lines.append(line)
    points.append(point)

def init():
    for line, point in zip(lines, points):
        line.set_data([], [])
        line.set_3d_properties([])
        point.set_data([], [])
        point.set_3d_properties([])
    return lines + points

def update(frame):
    for i in range(n_part):
        x = kp_smooth[i][:frame+1]
        y = ki_smooth[i][:frame+1]
        z = kd_smooth[i][:frame+1]

        lines[i].set_data(x, y)
        lines[i].set_3d_properties(z)

        # Punto actual
        points[i].set_data([x[-1]], [y[-1]])
        points[i].set_3d_properties([z[-1]])
    return lines + points

ani = FuncAnimation(fig, update, frames=n_frames,
                    init_func=init, blit=False, interval=50)


from matplotlib.animation import PillowWriter
import subprocess
ani.save("C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/animacion4.gif", writer=PillowWriter(fps=20))


plt.show(block=True)