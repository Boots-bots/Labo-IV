import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings.imports import*
from settings.estética import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

# Mediciones BM
BM = []
for i in range(1, 6):  #BM3 (no) 
    BM.append(pd.read_csv(folder+ "/Presión/" + f"BM{i}.csv", index_col=["Tiempo"]))

for i in (1,2,4,5):
    plt.figure(figsize=(6, 4))
    plt.title(f"BM{i}")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Presión [Torr]")
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.plot(BM[i-1].index, BM[i-1]["Presión"],".k", label="Mediciones BM")
    # plt.legend()

# plt. figure(figsize=(8, 6))
# plt.title("BM")
# plt.xlabel("Tiempo [s]")
# plt.ylabel("Presión [Torr]")
# plt.grid(color="gray", linestyle="-", linewidth=0.5)
# plt.plot(BM[0].index, BM[0]["Presión"],".", label="Mediciones BM1")
# plt.plot(BM[1].index + 27, BM[1]["Presión"],".", label="Mediciones BM2") # corrección de tiempo +27
# plt.plot(BM[3].index + 18, BM[3]["Presión"],".", label="Mediciones BM4") # corrección de tiempo +18
# plt.plot(BM[4].index - 2.6, BM[4]["Presión"],".", label="Mediciones BM5") # corrección de tiempo -2.6
# plt.legend()

plt.show(block=True)

