import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings.imports import*
from settings.estética import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

pcteBM = []
for i in range(1, 6):  #pcteBM2 (no)
    pcteBM.append(pd.read_csv(folder+ "/Presión/" + f"pcteBM{i}.csv", index_col=["Tiempo"]))

F = pd.read_csv(folder+ "/Presión/" + f"F.csv", index_col=["Tiempo"]) # pcte BM

pcteBD = []
for i in range(1, 6):
    pcteBD.append(pd.read_csv(folder+ "/Presión/" + f"pcteBD{i}.csv", index_col=["Tiempo"]))

def fuga(t,C,V,p0,pe):
    "C conductancia de predidas"
    "V volumen de la cámara"
    "p0 presión inicial"
    "pe presión externa"
    return pe + (p0 - pe) * np.exp(-t*C / V)

def desgase(t,Q,V,p0):
    "Q caudal de gas entrante debido a desgase"
    "V volumen de la cámara"
    "p0 presión inicial"
    return p0 + Q * t / V

def perdidas(t,C,Q,V,p0,pe,F,D):
    return F*fuga(t,C,V,p0,pe) + D*desgase(t,Q,V,p0) 

exit()

plt.figure(figsize=(8, 6))
# plt.title("pcte BM")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(pcteBM[0].index, pcteBM[0]["Presión"],".", label="pcteBM1")
plt.plot(pcteBM[2].index, pcteBM[2]["Presión"],".", label="pcteBM3")
plt.plot(pcteBM[3].index, pcteBM[3]["Presión"],".", label="pcteBM4")
plt.plot(pcteBM[4].index, pcteBM[4]["Presión"],".", label="pcteBM5")
plt.legend()

plt.figure(figsize=(8, 6))
plt.title("F (pcte BM)")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.plot(F.index, F["Presión"],".", label="Mediciones F")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.legend()

plt.figure(figsize=(8, 6))
# plt.title("pcte BD")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(pcteBD[0].index, pcteBD[0]["Presión"],".", label="pcteBD1")
plt.plot(pcteBD[1].index, pcteBD[1]["Presión"],".", label="pcteBD2")
plt.plot(pcteBD[2].index, pcteBD[2]["Presión"],".", label="pcteBD3")
# plt.plot(pcteBD[3].index, pcteBD[3]["Presión"],".", label="pcteBD4")
plt.plot(pcteBD[4].index, pcteBD[4]["Presión"],".", label="pcteBD5")
plt.legend()

plt.figure(figsize=(8, 6))
plt.title("pcte BD 4")
plt.plot(pcteBD[3].index, pcteBD[3]["Presión"],".", label="pcteBD4")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.legend()

plt.show(block=True)