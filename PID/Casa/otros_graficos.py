import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime
import glob

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"
selected_file = "cuadrada-I_170_20250612_094258.csv"

file_path = os.path.join(folder, selected_file)
df = pd.read_csv(file_path)


fig, axs = plt.subplots(2, 1, figsize=(6, 4), sharex=True)
axs[0].plot(df['tiempo'][1:], df['posicion'][1:],color='blue')
axs[0].set_ylabel('Posición [pixeles]')
axs[0].set_title('Control en función del tiempo')
axs[0].grid(True)
axs[1].plot(df['tiempo'], df['señal'], color='green')
axs[1].set_ylabel('Control %', rotation=0)
axs[1].axhline(0, linestyle='--', color='red') 
axs[1].axhline(255, linestyle='--', color='red', label= f'Rango = 0-255') 
axs[1].grid(True)
plt.tight_layout()
plt.show()
