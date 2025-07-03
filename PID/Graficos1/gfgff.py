import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/PID/D1/Impulsos/"
dataframes = []

for i in (1, 2, 3):
    selected_file = f"cuadrada-prendido_{i}.csv"
    file_path = os.path.join(folder, selected_file)
    df = pd.read_csv(file_path)
    dataframes.append(df)

fig, ax1 = plt.subplots(figsize=(10, 6))

# Graficar las posiciones con etiqueta solo en la primera
for i, df in enumerate(dataframes):
    label = "Posición" if i == 0 else None
    ax1.plot(df["tiempo"][1:], df["posicion"][1:], color='blue', linewidth=2, label=label)

ax1.set_xlabel("Tiempo [s]", fontsize=16)
ax1.set_ylabel("Posición [pixeles]", fontsize=16)
ax1.tick_params(axis='both', labelsize=14)
ax1.grid(True)

# Segundo eje Y para control
ax2 = ax1.twinx()
ax2.plot(dataframes[0]["tiempo"], dataframes[0]["señal"], color='red', linewidth=2, label="Control")
ax2.set_ylabel("Control [%]", fontsize=16)
ax2.tick_params(axis='y', labelsize=12)

# Combinar leyendas de ambos ejes y ponerla dentro del gráfico
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc="lower right", fontsize=18)

plt.tight_layout()
plt.show()