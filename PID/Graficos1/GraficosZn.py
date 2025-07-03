import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re

def por(x):
    return x*100/255

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/D2/SpV/Sierra/Con_Pso/"

folder = folder 

DF = []

unidad = "pixeles"
sp = 300
tch = 488
a = 160

plt.figure()
# plt.axhline(sp, linestyle='--', color='red', label= f'Sp = {sp:.0f} {unidad}') 
# plt.axhline(tch, linestyle='--', color='k', labe= f'Techo = {tch:.0f} {unidad}') 
for i in (0,):
    index = i
    selected_file = f"Kpso_Kp5.11_Ki8.31_Kd4.70 _Set500_ISE221369.29_20250619_115820.csv" # nombre del archivo a cargar
    file_path = os.path.join(folder, selected_file)
    df = pd.read_csv(file_path)
    DF.append(df)
    # si tiene columnas [tiempo, posicion, error, P, I, D, control, Kp, Ki, Kd, ISE]

    # print(df.head())

    # Extraer los valores característicos 
    # kp = df['Kp'].iloc[0]
    # ki = df['Ki'].iloc[0]
    # kd = df['Kd'].iloc[0]
    # ise = df['ITAE'].iloc[0]

    # print(f"Kp = {kp}, Ki = {ki}, Kd = {kd}, ISE = {ise}")

    # Graficar posición vs tiempo
    if i == 0:
        # plt.fill_between(df['tiempo'][1:],0,35, color = "moccasin", alpha = 0.3, label = "Efecto de Borde")
        # plt.fill_between(df['tiempo'][1:], tch-35, tch, color = "moccasin", alpha = 0.3)
        plt.plot(df['tiempo'][1:], df['posicion'][1:], "b" , label='Posición')
    plt.plot(df['tiempo'][1:], df['posicion'][1:], "b") # , label='Posición')
    plt.plot(df['tiempo'][1:], df['setpoint'][1:] , color = "r", label = f"Setpoint")
    # plt.axvline(df['tiempo'][a], linestyle='--', color='orange')
    plt.xlabel('Tiempo [s]', fontsize = 16)
    plt.ylabel(f'Posición [{unidad}]', fontsize  =16)
    # plt.title(f'Posición vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
    plt.legend(loc = "lower right" ,fontsize=18) #loc = "upper right")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.tight_layout()


# señal vs timepo
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6, 3))
for df in DF:
    # Graficar cada variable
    u = np.mean(por(df['control'][a:]))
    axs[0].axhline(0, linestyle='--', color='red') 
    axs[0].axhline(por(255), linestyle='--', color='red', label= f'Rango = 0-255') 
    # axs[0].axhline(u, linestyle='--', color='orange', label= f'Media {u:.0f}') 
    axs[0].plot(df['tiempo'], por(df['control']), color='blue')
    axs[0].set_ylabel('Control %', fontsize = 16)
    axs[0].tick_params(axis='y', labelsize=14)
    axs[1].tick_params(axis='y', labelsize=14)
    # axs[0].set_title('Control en función del tiempo')
    axs[0].grid(True)
    axs[1].plot(df['tiempo'], por(df['P']), color='green')
    axs[1].set_ylabel('P', rotation=0, fontsize = 16)
    axs[1].grid(True)
    axs[1].tick_params(axis='y', labelsize=14)
    # axs[2].plot(df['tiempo'], por(df['I']), color='orange')
    # axs[2].set_ylabel('I', rotation=0)
    # axs[2].grid(True)
    # axs[2].tick_params(axis='y', labelsize=14)
    # axs[3].plot(df['tiempo'], por(df['D']), color='red')
    # axs[3].set_ylabel('D', rotation=0)
    # axs[3].set_xlabel('Tiempo [s]', fontsize = 16)
    axs[1].tick_params(axis='x', labelsize=14)
    # axs[3].tick_params(axis='y', labelsize=14)
    axs[1].grid(True)
    plt.tight_layout()

print(u)
# Graficar error vs tiempo
plt.figure(figsize=(10, 5))
for df in DF:
    plt.plot(df['tiempo'], df['error'], label='Error', color='red')
    # plt.axhline(ise/len(df['tiempo']), linestyle='--', color='blue', label='ISE/len') 
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Error Cuadrático')
    # plt.title(f'Error vs Tiempo\nKp={kp}, Ki={ki}, Kd={kd}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
plt.show(block= True)

