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
    return (p0 + pf) * np.exp(-t * S / V) + pf

def exp(x,a,b,c,d):
    return a * np.exp(-b*(x-c)) + d

ejex = np.linspace(0, 1000, 1000)
ejex2 = np.linspace(0, 325, 1000)

plt.figure(figsize=(6, 4))
# plt.title(f"BD{i}")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.axhline(y = 2.7e-5, color = "k", linestyle = "--", label = "saturación", alpha=0.5)
plt.plot(BD[1].index, BD[1]["Presión"],".k", label="Medicion BD2")
plt.plot(ejex, exp(ejex, 2.7e-5, 0.02, 300, 0.4e-5), color="g")
plt.plot(ejex2, exp(ejex2, -2.7e-5, -0.007, 370, 3.9e-5), color="r")
plt.xlim(130,800)
plt.ylim(0.2e-5, 4e-5)
plt.legend()

plt.show(block=True)