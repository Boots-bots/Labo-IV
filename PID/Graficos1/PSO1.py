import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/Dia1/Med/"
# folder = folder + "/PSO1(5_3)/"
# folder = folder + "/PSO2(10_5)/"
folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/Dia3/ITAE/itae_k_largo/"


filenames = [f for f in os.listdir(folder) if f.startswith("Kp") and f.endswith(".csv")]
filenames = sorted(filenames, key=lambda name: re.search(r"_(\d{8})_(\d{6})", name).group(0))


sp = 270
unidad = "pixeles"

# Función para obtener número de partícula
def get_particula(idx):
    return (idx % 5) + 1

# Procesar de a 3 archivos
for i in range(0, len(filenames), 5):
    files_batch = filenames[i:i+5]
    if len(files_batch) < 5:
        print(f"Saltando grupo incompleto en índice {i}")
        continue

    fig_pos, axs_pos = plt.subplots(5, 1, figsize=(10, 8), sharex=True)
    fig_control, axs_control = plt.subplots(5, 4, figsize=(7, 5), sharex='col')
    fig_error, axs_error = plt.subplots(5, 1, figsize=(7, 4), sharex=True)

    for j, filename in enumerate(files_batch):
        idx = i + j  # índice global
        particula = get_particula(idx)
        iteracion = i//5 + 1

        file_path = os.path.join(folder, filename)
        df = pd.read_csv(file_path)

        kp = df['Kp'].iloc[0]
        ki = df['Ki'].iloc[0]
        kd = df['Kd'].iloc[0]
        ise = df['ITAE'].iloc[0]

        tiempo = df['tiempo']

        # Posición vs tiempo
        axs_pos[j].plot(tiempo, df['posicion'], label=f'Partícula {particula}, Iter {iteracion}\nKp={kp:.2f}, Ki={ki:.2f}, Kd={kd:.2f}')
        axs_pos[j].axhline(sp, linestyle='--', color='red', label='Setpoint')
        axs_pos[j].set_ylabel('Posición')
        axs_pos[j].legend()
        axs_pos[j].grid(True)

        # Control y PID
        axs_control[j, 0].plot(tiempo, df['control'], color='blue')
        axs_control[j, 0].axhline(0, linestyle='--', color='gray')
        axs_control[j, 0].axhline(255, linestyle='--', color='gray')
        axs_control[j, 0].set_ylabel('Control')
        axs_control[j, 0].set_title(f'Partícula {particula}, Iter {iteracion}')
        axs_control[j, 0].grid(True)

        axs_control[j, 1].plot(tiempo, df['P'], color='green')
        axs_control[j, 1].set_ylabel('P')
        axs_control[j, 1].grid(True)

        axs_control[j, 2].plot(tiempo, df['I'], color='orange')
        axs_control[j, 2].set_ylabel('I')
        axs_control[j, 2].grid(True)

        axs_control[j, 3].plot(tiempo, df['D'], color='red')
        axs_control[j, 3].set_ylabel('D')
        axs_control[j, 3].grid(True)

        # Error
        axs_error[j].plot(tiempo, df['error'], color='red', label=f'Partícula {particula}, Iter {iteracion}\nITAE={ise:.1f}')
        axs_error[j].set_ylabel('Error')
        axs_error[j].legend()
        axs_error[j].grid(True)

    axs_pos[-1].set_xlabel("Tiempo [s]")
    axs_control[-1, 0].set_xlabel("Tiempo [s]")
    axs_control[-1, 1].set_xlabel("Tiempo [s]")
    axs_control[-1, 2].set_xlabel("Tiempo [s]")
    axs_control[-1, 3].set_xlabel("Tiempo [s]")
    axs_error[-1].set_xlabel("Tiempo [s]")

    fig_pos.suptitle(f'Posición vs Tiempo - Archivos {i}-{i+2}')
    fig_control.suptitle(f'Control y PID - Archivos {i}-{i+2}')
    fig_error.suptitle(f'Error vs Tiempo - Archivos {i}-{i+2}')

    fig_pos.tight_layout()
    fig_control.tight_layout()
    fig_error.tight_layout()
    plt.show()
