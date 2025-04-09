import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings.imports import*
from settings.estética import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

# Mediciones BD
BD = []
for i in range(1, 5):
    BD.append(pd.read_csv(folder+ "/Presión/" + f"BD{i}.csv", index_col=["Tiempo"]))

def bombeo(t,S,V,p0,pf):
    "S velocidad de bombeo"
    "V volumen de la cámara"
    "p0, pf presión inicial, final"
    return (p0 + pf) * np.exp(t * S / V) + pf

exit()

for i in (1,2,3,4):
    plt.figure(figsize=(6, 4))
    plt.title(f"BD{i}")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Presión [Torr]")
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.plot(BD[i-1].index, BD[i-1]["Presión"],".k", label="Mediciones BD")
    # plt.legend()

plt. figure(figsize=(8, 6))
plt.title("BD")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(BD[0].index, BD[0]["Presión"],".", label="Mediciones BD1")
plt.plot(BD[2].index, BD[2]["Presión"],".", label="Mediciones BD3") # corrección de tiempo +18
plt.plot(BD[3].index+1.2, BD[3]["Presión"],".", label="Mediciones BD4") # corrección de tiempo +1.2
plt.legend()

plt.show(block=True)


