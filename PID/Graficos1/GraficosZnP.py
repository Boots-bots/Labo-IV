import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/Dia1/Med/"

DF = []
plt.figure()
for i in range(1,6):
    selected_file = f"Kc3.5_{i}.csv" # nombre del archivo a cargar

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

    plt.plot(df['tiempo'][1:], df['posicion'][1:], "b", label='Posición')
    # plt.axhline(sp, linestyle='--', color='red', label= f'Sp = {sp}:.1f {unidad}') 
    plt.xlabel('Tiempo [s]')
    plt.ylabel(f'Posición [{unidad}]')
    plt.title(f'Posición vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # señal vs timepo
fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
for df in DF:
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
for df in DF:
    plt.plot(df['tiempo'], df['error'], label='Error', color='red')
    # plt.axhline(ise/len(df['tiempo']), linestyle='--', color='blue', label='ISE/len') 
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Error')
    plt.title(f'Error vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
plt.show(block= True)

###############

DF = []
plt.figure()
for i in range(1,6):
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

    plt.plot(df['tiempo'][1:], df['posicion'][1:], "b", label='Posición')
    # plt.axhline(sp, linestyle='--', color='red', label= f'Sp = {sp}:.1f {unidad}') 
    plt.xlabel('Tiempo [s]')
    plt.ylabel(f'Posición [{unidad}]')
    plt.title(f'Posición vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # señal vs timepo
fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
for df in DF:
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
for df in DF:
    plt.plot(df['tiempo'], df['error'], label='Error', color='red')
    # plt.axhline(ise/len(df['tiempo']), linestyle='--', color='blue', label='ISE/len') 
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Error')
    plt.title(f'Error vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
plt.show(block= True)