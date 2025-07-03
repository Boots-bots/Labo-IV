# Imports
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/D2/SpV/"

#  Graficos Dia 1
# Archivos sin nombre, cargar archivos sin nombre, con columnas [tiempo, posicion, error, P, I, D, control, Kp, Ki, Kd, ISE]   # version 3.0 [setpoint]

folder = folder + "Lineal/"

filenames = [f for f in os.listdir(folder) if f.startswith("Kp") and f.endswith(".csv")]
filenames = sorted(filenames, key=lambda name: re.search(r"_(\d{8})_(\d{6})", name).group(0))

for idx, name in enumerate(filenames):
    print(f"{idx}: {name}")


unidad = "pixeles"
tolerancia = 5 #8.1944444444444444

colores = ["r","r","g","b","b"]
colores = ["a","b","b", "r","g"]

# filenames.reverse()
# colores.reverse()

DF=[]
for i in (3,4): # range(len(filenames)):
    index = i
    selected_file = filenames[index]

    file_path = os.path.join(folder, selected_file)
    df = pd.read_csv(file_path)
    DF.append(df)
    # print(df.head())

    # Extraer los valores característicos 
    kp = df['Kp'].iloc[0]
    ki = df['Ki'].iloc[0]
    kd = df['Kd'].iloc[0]
    ise = df['ISE'].iloc[0]

    print(f"Kp = {kp}, Ki = {ki}, Kd = {kd}, ISE = {ise}")


plt.figure(figsize=(10,7))
for n in (0,1):
# Graficar posición vs tiempo
# plt.axhline(465,linestyle='--', color='gray', label = "Techo")
# plt.fill_between(DF[n]['tiempo'][1:], DF[n]['setpoint'][1:]-60 - tolerancia, DF[n]['setpoint'][1:]-60 + tolerancia, alpha = 0.2, color = colores[3])
    if n == 0:
        plt.plot(DF[n]['tiempo'][1:], DF[n]['setpoint'][1:] -60 , color = colores[3], label = f"Setpoint")
        plt.plot(DF[n]['tiempo'][1:], DF[n]['posicion'][1:], color = colores[2], label = f"Posición")
    plt.plot(DF[n]['tiempo'][1:], DF[n]['setpoint'][1:] -60 , color = colores[3])
    plt.plot(DF[n]['tiempo'][1:], DF[n]['posicion'][1:], color = colores[2])
plt.xlabel('Tiempo [s]', fontsize = 16)
plt.ylabel(f'Posición [{unidad}]', fontsize = 16)
# plt.title(f'Setpoint Lineal\nKp={kp}, Ki={ki:.2f}, Kd={kd}')
# plt.ylim(-5,500)
plt.legend(fontsize = 18, loc = "lower right")
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.tight_layout()

plt.show()
