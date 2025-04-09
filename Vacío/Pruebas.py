# imports
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

# Pruebas

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


