import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from settings.imports import*
from settings.estética import*
from settings.ajustes import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

P = []
for i in (1,2,3,4,5):
    P.append(pd.read_csv(folder+ "/NO/" + f"P{i}.csv"))  # {"tiempo":tiempoP, "presion":presion}
R = []
for i in (1,2,3,4,5):
    R.append(pd.read_csv(folder+ "/NO/" + f"R{i}.csv"))    # {"tiempo":tiempoR, "resistencia":resistencia, "temperatura":temperatura}

indices_inicio = R[2].index[R[2]['tiempoR'] == 0].tolist()

# if len(indices_inicio) != 4:
#     raise ValueError(f"Se esperaban 4 mediciones, pero se encontraron {len(indices_inicio)} valores de tiempo = 0")

df_m1 = R[2].loc[indices_inicio[0]:indices_inicio[2]-1].reset_index(drop=True)
df_m2 = R[2].loc[indices_inicio[2]:indices_inicio[3]-1].reset_index(drop=True)
df_m3 = R[2].loc[indices_inicio[3]:indices_inicio[4]-1].reset_index(drop=True)
df_m4 = R[2].loc[indices_inicio[4]:].reset_index(drop=True)

df_1 = P[2].loc[indices_inicio[0]:indices_inicio[2]-1].reset_index(drop=True)
df_2 = P[2].loc[indices_inicio[2]:indices_inicio[3]-1].reset_index(drop=True)
df_3 = P[2].loc[indices_inicio[3]:indices_inicio[4]-1].reset_index(drop=True)
df_4 = P[2].loc[indices_inicio[4]:].reset_index(drop=True)

df_m1 = df_m1.rename(columns={'tiempoR': 'tiempo'})
df_m2 = df_m2.rename(columns={'tiempoR': 'tiempo'})
df_m3 = df_m3.rename(columns={'tiempoR': 'tiempo'})
df_m4 = df_m4.rename(columns={'tiempoR': 'tiempo'})

df_1 = df_1.rename(columns={'tiempoP': 'tiempo'})
df_2 = df_2.rename(columns={'tiempoP': 'tiempo'})
df_3 = df_3.rename(columns={'tiempoP': 'tiempo'})
df_4 = df_4.rename(columns={'tiempoP': 'tiempo'})

R = [df_m1, df_m2, df_m3, df_m4, R[3], R[4]]
P = [df_1, df_2, df_3, df_4, P[3], P[4]]

for i in range(len(P)):
    P[i].to_csv(folder +f"P{i}.csv", index=False, header=True)
    R[i].to_csv(folder +f"R{i}.csv", index=False, header=True)

for i in (0,1,2,3,4,5):
    plt.figure()
    plt.plot(P[i]["tiempo"], P[i]["presion"], label="P1")
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Temperatura [°C]")
    plt.title(f"P{i+1}")
    plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 
plt.show(block=True)

for i in (0,1,2,3,4,5):
    plt.figure()
    plt.plot(R[i]["tiempo"], R[i]["temperatura"], label="R1")
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Temperatura [°C]")
    plt.title(f"R{i+1}")
    plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 
plt.show(block=True)


