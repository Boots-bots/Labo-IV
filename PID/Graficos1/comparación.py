import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/D1/"

def por(x):
    return x*100/255

a = 160
pso = pd.read_csv(os.path.join(folder, "resPSO1.csv"))

DF = []
plt.figure()
for i in (1,):
    selected_file = f"Zn_Set300_{i}.csv" # nombre del archivo a cargar

    file_path = os.path.join(folder, selected_file)
    df = pd.read_csv(file_path)
    DF.append(df)
    # si tiene columnas [tiempo, posicion, error, P, I, D, control, Kp, Ki, Kd, ISE]

    # print(df.head())

    # Extraer los valores característicos 
    kp = df['Kp'].iloc[0]
    ki = df['Ki'].iloc[0]
    kd = df['Kd'].iloc[0]
    ise = df['ISE'].iloc[0]

    print(f"Kp = {kp}, Ki = {ki}, Kd = {kd}, ISE = {ise}")

    unidad = "pixeles"
    sp = 300

    # Graficar posición vs tiempo
    plt.axvline(df['tiempo'][a], linestyle='--', color='orange')
    plt.plot(df['tiempo'][1:], df['posicion'][1:], "b", label='Posición')
    plt.plot(pso['tiempo'][1:], pso['posicion'][1:], "b")
    plt.axhline(sp, linestyle='--', color='red', label= f'Sp = {sp:.1f} {unidad}') 
    plt.xlabel('Tiempo [s]')
    plt.ylabel(f'Posición [{unidad}]')
    plt.title(f'Posición vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # señal vs timepo
fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
axs[0].plot(pso['tiempo'], por(pso['control']), color='blue')
axs[1].plot(pso['tiempo'], pso['P'], color='green')
axs[3].plot(pso['tiempo'], pso['D'], color='red')
for df in DF:
    # Graficar cada variable
    u = np.mean(por(pso['control'][a:]))
    axs[0].axhline(0, linestyle='--', color='red') 
    axs[0].axhline(100, linestyle='--', color='red', label= f'Rango = 0-255') 
    axs[0].plot(df['tiempo'], por(df['control']), color='blue')
    axs[0].axhline(u, linestyle='--', color='orange', label= f'Media {u:.0f}') 
    axs[0].set_ylabel('Control %')
    axs[0].set_title('Control en función del tiempo')
    axs[0].grid(True)
    axs[1].plot(df['tiempo'], df['P'], color='green')
    axs[1].set_ylabel('P', rotation=0)
    axs[1].grid(True)
    axs[2].plot(df['tiempo'], df['I'], color='orange')
    axs[2].set_ylabel('I', rotation=0)
    axs[2].grid(True)
    axs[3].plot(df['tiempo'], df['D'], color='red')
    axs[3].set_ylabel('D', rotation=0)
    axs[3].set_xlabel('Tiempo [s]')
    axs[3].grid(True)
    plt.tight_layout()

print(u)
# Graficar error vs tiempo

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

fig, ax = plt.subplots()  # figura principal

# Plot principal
for df in DF:
    ax.plot(pso['tiempo'], pso['error'], color='red', label="PSO")
    ax.plot(df['tiempo'], df['error'], label='ZN', color='blue')

ax.set_xlabel('Tiempo [s]')
ax.set_ylabel('Error Cuadrático')
ax.legend()
ax.grid(True)

# Crear el subplot de zoom con tamaño personalizado
# [x0, y0, ancho, alto] en fracción del gráfico principal
axins = inset_axes(ax, width="90%", height="90%", bbox_to_anchor=(0.5, 0.4, 0.4, 0.3), bbox_transform=ax.transAxes)

# Dibujar datos en el zoom
for df in DF:
    axins.plot(pso['tiempo'], pso['error'], color='red')
    axins.plot(df['tiempo'], df['error'], color='blue')

# Región del zoom
x1, x2 = 20, 25
y1, y2 = 0, 70
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.grid(True)

# Conectar con líneas más oscuras y gruesas
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="black", lw=0.8)

plt.tight_layout()

plt.show(block= True)