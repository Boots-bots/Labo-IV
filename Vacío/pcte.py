import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings.imports import*
from settings.estética import*
from settings.ajustes import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

pcteBM = []
for i in range(1, 6):  #pcteBM2 (no)
    pcteBM.append(pd.read_csv(folder+ "/Presión/" + f"pcteBM{i}.csv", index_col=["Tiempo"]))

F = pd.read_csv(folder+ "/Presión/" + f"F.csv", index_col=["Tiempo"]) # pcte BM

pcteBD = []
for i in range(1, 6):
    pcteBD.append(pd.read_csv(folder+ "/Presión/" + f"pcteBD{i}.csv", index_col=["Tiempo"]))

def fuga(t,CV,p0): # CV = C/V PE = 750
    "C conductancia de predidas"
    "V volumen de la cámara"
    "p0 presión inicial"
    "pe presión externa"
    return 750 + (p0 - 750) * np.exp(-t*CV)

def desgase(t,QV,p0): # QV = Q/V
    "Q caudal de gas entrante debido a desgase"
    "V volumen de la cámara"
    "p0 presión inicial"
    return p0 + t * QV

def perdidas(t,CV,QV,p0,c): # CV = C/V ; QV = Q/V ; PE = 750 ; c = fuga  1 - c = desgase
    return (c)*fuga(t,CV,p0) + (1-c  )*desgase(t,QV,p0) 

def error(df):
    p = np.array(df["Presión"].values)
    std = []
    for y in p:                  # error sensor 
        # std.append(0.05*y)
        if y > 7.5e-4:
            std.append(0.15*y)
        elif y > 75:
            std.append(0.05*y)
        else:
            std.append(0.30*y)

    for i in range(len(std)-1):  # error temporal
        a = (p[i+1] - p[i])/np.sqrt(12)
        # if a > std[i]:
        std[i] = std[i] + a

    return np.array(std)

# ajustes

Parametros, Errores = [], []
Chis, Pvals = [], []
for i in range(len(pcteBM)):
    pop, cov = curve_fit(perdidas, pcteBM[i].index.values, pcteBM[i]["Presión"].values, sigma = error(pcteBM[i]) , p0=[3e-6,1e-6,pcteBM[i]["Presión"][0],1/2], absolute_sigma=True)
    Parametros.append(pop)
    Errores.append(np.sqrt(np.diag(cov)))
    chi, pv, nu = chi2_pvalor(pcteBM[i].index.values, pcteBM[i]["Presión"].values, error(pcteBM[i]), perdidas(pcteBM[i].index.values, *pop), 2)
    Chis.append(chi/nu)
    Pvals.append(pv)
    # residuos(perdidas, pop, pcteBM[i].index.values, pcteBM[i]["Presión"].values, error(pcteBM[i]), grafico = True)


plt.show(block=True)

# resultados
for i in range(len(pcteBM)): 
    if i!=1:
        print("pcte BM", i+1)
        print("pvalor: ", Pvals[i], "Chi: ", Chis[i])
        print("C/V: ", Parametros[i][0], "±", Errores[i][0],"Q/V: ", Parametros[i][1], "±", Errores[i][1], "p0: ", Parametros[i][2], "±", Errores[i][2], "c: ", Parametros[i][3], "±", Errores[i][3])

color = ("b","orange","g","k","r")

ejex = np.linspace(0, 1e8, 10000)

plt.figure(figsize=(8, 6))
# plt.title("pcte BM")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
for i in range(len(pcteBM)):
    if i != 1:
        # ejex = np.linspace(np.min(pcteBM[i].index), np.max(pcteBM[i].index), 10000)
        plt.fill_between(pcteBM[i].index, pcteBM[i]["Presión"] - error(pcteBM[i]), pcteBM[i]["Presión"] + error(pcteBM[i]), alpha=0.3)
        plt.plot(pcteBM[i].index, pcteBM[i]["Presión"], ".", color = color[i], label=f"Mediciones pcteBM{i+1}")
        plt.plot(ejex, perdidas(ejex, *Parametros[i]), color = color[i])
plt.ylim(np.min(pcteBM[i]["Presión"])*0.8, np.max(pcteBM[i]["Presión"])*1.2)
plt.xlim(np.min(pcteBM[2].index), np.max(pcteBM[2].index))
plt.legend()

for i in range(len(pcteBM)):
    if i != 1:
        ejex = np.linspace(np.min(pcteBM[i].index), np.max(pcteBM[i].index), 10000)
        plt.figure(figsize=(8, 6))
        # plt.title(f"pcte BD{i+1}")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Presión [Torr]")
        plt.grid(color="gray", linestyle="-", linewidth=0.5)
        plt.fill_between(pcteBM[i].index, pcteBM[i]["Presión"] - error(pcteBM[i]), pcteBM[i]["Presión"] + error(pcteBM[i]), alpha=0.3)
        plt.plot(pcteBM[i].index, pcteBM[i]["Presión"], ".", color = color[i], label=f"Mediciones pcteBM{i+1}")
        plt.plot(ejex, perdidas(ejex, *Parametros[i]), color = color[i])
        # plt.ylim(np.min(pcteBM[i]["Presión"])*0.8, np.max(pcteBM[i]["Presión"])*1.2)
        plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 

plt.show(block=True)

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