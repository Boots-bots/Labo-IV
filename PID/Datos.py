#%% Imports
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/Dia2/"

#%%  Graficos Dia 1

# Archivos sin nombre, cargar archivos sin nombre, con columnas [tiempo, posicion, error, P, I, D, control, Kp, Ki, Kd, ISE]   # version 3.0 [setpoint]

folder = folder + "/PSO3/"

filenames = [f for f in os.listdir(folder) if f.startswith("Kp") and f.endswith(".csv")]
filenames = sorted(filenames, key=lambda name: re.search(r"_(\d{8})_(\d{6})", name).group(0))

for idx, name in enumerate(filenames):
    print(f"{idx}: {name}")

#%%

index = 0 # seleccionar archivo, por orden de horario
sp = 300

selected_file = filenames[index]

file_path = os.path.join(folder, selected_file)
df = pd.read_csv(file_path)

# print(df.head())

# Extraer los valores característicos 
kp = df['Kp'].iloc[0]
ki = df['Ki'].iloc[0]
kd = df['Kd'].iloc[0]
ise = df['ISE'].iloc[0]

print(f"Kp = {kp}, Ki = {ki}, Kd = {kd}, ISE = {ise}")

unidad = "pixeles"

c = 100

# Graficar posición vs tiempo
plt.figure()
plt.plot(df['tiempo'][1:], df['posicion'][1:], "b", label='Posición')
plt.axhline(sp, linestyle='--', color='red', label= f'Sp = {sp} {unidad}') 
plt.axvline(df['tiempo'][c])
plt.xlabel('Tiempo [s]')
plt.ylabel(f'Posición [{unidad}]')
plt.title(f'Posición vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
plt.legend()
plt.grid(True)
plt.tight_layout()

# señal vs timepo
fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)

a = np.mean(df['control'][c:])

# Graficar cada variable
axs[0].axhline(0, linestyle='--', color='red') 
axs[0].axhline(255, linestyle='--', color='red', label= f'Rango = 0-255')
axs[0].axhline(a, linestyle='--', color='green', label= f'Señal Eff {a:.0f}') 
axs[0].plot(df['tiempo'], df['control'], color='blue')
axs[0].set_ylabel('Control %')
axs[0].legend()
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

# Graficar error vs tiempo
plt.figure(figsize=(10, 5))
plt.plot(df['tiempo'], df['error'], label='Error', color='red')
# plt.axhline(ise/len(df['tiempo']), linestyle='--', color='blue', label='ISE/len') 
plt.xlabel('Tiempo [s]')
plt.ylabel('Error')
plt.title(f'Error vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



#%% Cargar archivos en particular

# folder = folder

selected_file = f"Zn_Set200.csv" # nombre del archivo a cargar

file_path = os.path.join(folder, selected_file)
df = pd.read_csv(file_path)

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
plt.figure()
plt.plot(df['tiempo'][1:], df['posicion'][1:], "b", label='Posición')
plt.axhline(sp, linestyle='--', color='red', label= f'Sp = {sp}:.1f {unidad}') 
plt.xlabel('Tiempo [s]')
plt.ylabel(f'Posición [{unidad}]')
plt.title(f'Posición vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
plt.legend()
plt.grid(True)
plt.tight_layout()

    # señal vs timepo
fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
    # Graficar cada variable
axs[0].axhline(0, linestyle='--', color='red') 
axs[0].axhline(255, linestyle='--', color='red', label= f'Rango = 0-255') 
axs[0].plot(df['tiempo'], df['control'], color='blue')
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

# Graficar error vs tiempo
plt.figure(figsize=(10, 5))
plt.plot(df['tiempo'], df['error'], label='Error', color='red')
# plt.axhline(ise/len(df['tiempo']), linestyle='--', color='blue', label='ISE/len') 
plt.xlabel('Tiempo [s]')
plt.ylabel('Error')
plt.title(f'Error vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#%% Graficos 2
# Cargar archivos en particular, impulsos

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/Dia1/Med/Impulsos/"

selected_file = "lineal.csv" # nombre del archivo a cargar

file_path = os.path.join(folder, selected_file)
df = pd.read_csv(file_path)

unidad = "pixeles"
# asuminendo columnas [tiempo, posicion, señal]

# señal vs timepo
fig, axs = plt.subplots(2, 1, figsize=(6, 4), sharex=True)

# Graficar cada variable
axs[0].plot(df['tiempo'][1:], df['posicion'][1:], color='blue')
axs[0].set_ylabel('Posición [{unidad}]')
axs[0].set_title('Control en función del tiempo')
axs[0].grid(True)
axs[1].plot(df['tiempo'], df['señal'], color='green')
axs[1].set_ylabel('Control %', rotation=0)
axs[1].axhline(0, linestyle='--', color='red') 
axs[1].axhline(255, linestyle='--', color='red', label= f'Rango = 0-255') 
axs[1].grid(True)
plt.tight_layout()
plt.show()
