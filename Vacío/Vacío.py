#%% imports
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings.imports import*
from settings.estética import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

prueba_fugas = pd.read_csv(folder + "Fugas.csv", index_col=["Tiempo"])
prueba_apagado = pd.read_csv(folder + "Apagado.csv", index_col=["Tiempo"])

def orden_magnitud(array):
    """
    Dado un array, crea otro array de unos ajustados al orden de magnitud
    de cada valor del array original.
    """
    array = np.array(array)
    # Calcular el orden de magnitud de cada valor
    orden_magnitud = np.floor(np.log10(np.abs(array)))  # Evitar log10(0)
    # Crear el nuevo array de unos ajustados al orden de magnitud
    nuevo_array = 10 ** orden_magnitud
    return nuevo_array

#%% Pruebas

# error1 = orden_magnitud(prueba_fugas["Presión"].values)
# error2 = orden_magnitud(prueba_apagado["Presión"].values)
error1 = 1e-6*np.ones(len(prueba_fugas["Presión"].values))
error2 = 1e-6*np.ones(len(prueba_apagado["Presión"].values))

fig, axs = plt.subplots(1, 2, figsize=(8, 6))  # 2 filas, 1 columna
# Subplot 1: Prueba de fugas
# axs[0].set_title("Prueba de Fugas")
axs[0].set_xlabel("Tiempo [s]")
axs[0].set_ylabel("Presión [Torr]")
axs[0].grid(color="gray", linestyle="-", linewidth=0.5)
axs[0].errorbar(prueba_fugas.index, prueba_fugas["Presión"], yerr = error1, fmt = ".k", label="Mediciones Fugas")
# axs[0].legend()
# Subplot 2: Prueba de apagado
# axs[1].set_title("Prueba de Apagado")
axs[1].set_xlabel("Tiempo [s]")
# axs[1].set_ylabel("Presión [Torr]")
axs[1].grid(color="gray", linestyle="-", linewidth=0.5)
axs[1].errorbar(prueba_apagado.index, prueba_apagado["Presión"], yerr = error2, fmt = ".k", label="Mediciones Apagado")
# axs[1].legend()
# Ajustar el espacio entre subplots
# plt.tight_layout()

plt.show(block=True)

#%% Mediciones
# Bomba Mecánica
BM = []
for i in range(1, 6):  #BM3 (no) 
    BM.append(pd.read_csv(folder+ "/Presión/" + f"BM{i}.csv", index_col=["Tiempo"]))
fugaBM = []
for i in range(1, 6):
    fugaBM.append(pd.read_csv(folder+ "/Presión/" + f"fugaBM{i}.csv", index_col=["Tiempo"]))
pcteBM = []
for i in range(1, 6):  #pcteBM2 (no)
    pcteBM.append(pd.read_csv(folder+ "/Presión/" + f"pcteBM{i}.csv", index_col=["Tiempo"]))

for i in (1,2,4,5):
    plt.figure(figsize=(6, 4))
    plt.title(f"BM{i+1}")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Presión [Torr]")
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.plot(BM[i-1].index, BM[i-1]["Presión"],".k", label="Mediciones BM")
    # plt.legend()

plt.figure(figsize=(8, 6))
plt.title("fugas BM")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(fugaBM[0].index, fugaBM[0]["Presión"],".", label="fugaBM1")
plt.plot(fugaBM[1].index, fugaBM[1]["Presión"],".", label="fugaBM2")
plt.plot(fugaBM[2].index, fugaBM[2]["Presión"],".", label="fugaBM3")
plt.plot(fugaBM[4].index, fugaBM[4]["Presión"],".", label="fugaBM5")
plt.legend()


plt.figure(figsize=(8, 6))
plt.title("pcte BM")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(pcteBM[0].index, pcteBM[0]["Presión"],".", label="pcteBM1")
plt.plot(pcteBM[2].index, pcteBM[2]["Presión"],".", label="pcteBM3")
plt.plot(pcteBM[3].index, pcteBM[3]["Presión"],".", label="pcteBM4")
plt.plot(pcteBM[4].index, pcteBM[4]["Presión"],".", label="pcteBM5")
plt.legend()

plt.show(block=True)
#%% Transición y otros

T = []
for i in range(1, 3):
    T.append(pd.read_csv(folder+ "/Presión/" + f"T{i}.csv", index_col=["Tiempo"]))
for i in range(1, 2):
    T.append(pd.read_csv(folder+ "/Presión/" + f"T{i}{i}.csv", index_col=["Tiempo"]))

K = pd.read_csv(folder+ "/Presión/" + f"K.csv", index_col=["Tiempo"])
F = pd.read_csv(folder+ "/Presión/" + f"F.csv", index_col=["Tiempo"])

plt.figure(figsize=(8, 6))
plt.title("Transición")
plt.xlabel("Tiempo [s]")

#%% Mediciones
# Bomba Difusora
BD = []
for i in range(1, 4):
    BD.append(pd.read_csv(folder+ "/Presión/" + f"BD{i}.csv", index_col=["Tiempo"]))
fugaBD = []
for i in range(1, 5):
    fugaBD.append(pd.read_csv(folder+ "/Presión/" + f"fugaBD{i}.csv", index_col=["Tiempo"]))
pcteBD = []
for i in range(1, 5):
    pcteBD.append(pd.read_csv(folder+ "/Presión/" + f"pctnBD{i}.csv", index_col=["Tiempo"]))