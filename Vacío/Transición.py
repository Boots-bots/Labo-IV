import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings.imports import*
from settings.estética import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"
  

K = pd.read_csv(folder+ "/Presión/" + f"K.csv", index_col=["Tiempo"])

# plt.figure(figsize=(8, 6)) 
# plt.title("K (apagado difusora)")
# plt.plot(K.index, K["Presión"],".", label="Mediciones K")
# plt.xlabel("Tiempo [s]")
# plt.ylabel("Presión [Torr]")
# plt.grid(color="gray", linestyle="-", linewidth=0.5)
# # plt.legend()
# plt.show(block=True)

# Transición 

T = []
for i in range(1, 4):
    T.append(pd.read_csv(folder+ "/Presión/" + f"T{i}.csv", index_col=["Tiempo"]))
for i in range(1, 3):
    T.append(pd.read_csv(folder+ "/Presión/" + f"T{i}{i}.csv", index_col=["Tiempo"]))

T[0] = T[0].iloc[:-1, :] # Eliminamos la última fila de T1 y T2, ceros
T[1] = T[1].iloc[:-1, :]

BD2 = pd.read_csv(folder+ "/Presión/" + f"BD2.csv", index_col=["Tiempo"])

# for i in range(1, 4):
#     plt.figure(figsize=(5, 3))
#     plt.title(f"T{i}")
#     plt.plot(T[i-1].index, T[i-1]["Presión"],".", label="Mediciones T")
#     plt.xlabel("Tiempo [s]")
#     plt.ylabel("Presión [Torr]")
#     plt.grid(color="gray", linestyle="-", linewidth=0.5)
#     #plt.legend()
# for i in range(1,3):
#     plt.figure(figsize=(5, 3))
#     plt.title(f"T{i}{i}")
#     plt.plot(T[i+2].index, T[i+2]["Presión"],".", label="Mediciones T")
#     plt.xlabel("Tiempo [s]")
#     plt.ylabel("Presión [Torr]")
#     plt.grid(color="gray", linestyle="-", linewidth=0.5)
#     #plt.legend()

# plt.figure(figsize=(8, 6))
# plt.title("BD2")
# plt.plot(BD2.index, BD2["Presión"],".", label="Mediciones T1")
# plt.xlabel("Tiempo [s]")
# plt.ylabel("Presión [Torr]")
# plt.grid(color="gray", linestyle="-", linewidth=0.5)
# # plt.legend()

# MATCH

plt.figure(figsize=(8, 6))
plt.title("Comparación de BD2")
plt.plot(BD2.index, BD2["Presión"],".", label="Mediciones BD2")
plt.plot(T[0].index-130, T[0]["Presión"],".", label="Mediciones T1")
plt.plot(T[3].index-50, T[3]["Presión"],".", label="Mediciones T11")
plt.plot(T[1].index-434, T[1]["Presión"],".", label="Mediciones T2")
plt.plot(T[4].index+275, T[4]["Presión"],".", label="Mediciones T22")
plt.plot(T[2].index+150, T[2]["Presión"],".", label="Mediciones T3")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.legend()

plt.show(block=True)


plt.figure(figsize=(8, 6))
plt.title("Mecanica T1 T11")
plt.plot(T[0].index, T[0]["Presión"],".", label="Mediciones T1")
plt.plot(T[3].index, T[3]["Presión"],".", label="Mediciones T11")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.legend()

plt.figure(figsize=(8, 6))
plt.title("Difusora T3 T22")
plt.plot(T[2].index, T[2]["Presión"],".", label="Mediciones T3")
plt.plot(T[4].index, T[4]["Presión"],".", label="Mediciones T22")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.legend()


plt.show(block=True)
