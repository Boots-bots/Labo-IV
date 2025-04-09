import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings.imports import*
from settings.estética import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

fugaBM = []
for i in range(1, 6):
    fugaBM.append(pd.read_csv(folder+ "/Presión/" + f"fugaBM{i}.csv", index_col=["Tiempo"]))

fugaBD = []
for i in range(1, 6):
    fugaBD.append(pd.read_csv(folder+ "/Presión/" + f"fugaBD{i}.csv", index_col=["Tiempo"]))

plt.figure(figsize=(8, 6))
# plt.title("fugas BM")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(fugaBM[0].index, fugaBM[0]["Presión"],".", label="fugaBM1")
plt.plot(fugaBM[1].index, fugaBM[1]["Presión"],".", label="fugaBM2")
plt.plot(fugaBM[2].index, fugaBM[2]["Presión"],".", label="fugaBM3")
plt.plot(fugaBM[4].index, fugaBM[4]["Presión"],".", label="fugaBM5")
plt.legend()

plt.figure(figsize=(8, 6))
# plt.title("fugas BD")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(fugaBD[0].index, fugaBD[0]["Presión"],".", label="fugaBD1")
plt.plot(fugaBD[1].index, fugaBD[1]["Presión"],".", label="fugaBD2")
plt.plot(fugaBD[2].index, fugaBD[2]["Presión"],".", label="fugaBD3")
plt.plot(fugaBD[3].index, fugaBD[3]["Presión"],".", label="fugaBD4")
plt.plot(fugaBD[4].index, fugaBD[4]["Presión"],".", label="fugaBD5")
plt.legend()

plt.figure(figsize=(8, 6))
plt.title("fuga BD 4")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(fugaBD[3].index, fugaBD[3]["Presión"],".", label="fugaBD4")

plt.show(block=True)