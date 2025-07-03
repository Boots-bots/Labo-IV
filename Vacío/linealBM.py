import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from settings.imports import*
from settings.estética import*
from settings.ajustes import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

# Mediciones BM
BM = []
for i in range(1, 6):  #BM3 (no) 
    BM.append(pd.read_csv(folder+ "/Presión/" + f"BM{i}.csv", index_col=["Tiempo"]))

def bombeo(t,SV,p0,pf):   #SV = S/V
    "S velocidad de bombeo"
    "V volumen de la cámara"
    "p0, pf presión inicial, final"
    return (p0 + pf) * np.exp(-t * SV) + pf

def bombeo2(t,b,a):   #
    return -t*b + np.log(a) 

def error(df):
    p = np.array(df["Presión"].values)
    std = []
    for y in p:                  # error sensor 
        std.append(0.07*np.log(y))
    #     if y > 7.5e-4:
    #         std.append(0.15*y)
    #     elif y > 75:
    #         std.append(0.05*y)
    #     else:
    #         std.append(0.30*y)

    # for i in range(len(std)-1):  # error temporal
    #     a = (p[i+1] - p[i])/np.sqrt(12)
    #     # if a > std[i]:
    #     std[i] = std[i] + a

    return np.array(std)

# S = 5,6 m^3/h ; 0.00156 m^3/s
# V = 4.5 L = 4.5e-3 m^3

BM[0] = BM[0].iloc[6:].reset_index(drop=True)
BM[1] = BM[1].iloc[4:].reset_index(drop=True)
BM[3] = BM[3].iloc[1:].reset_index(drop=True)
BM[4] = BM[4].iloc[7:].reset_index(drop=True)

Parametros, Errores = [], []
Chis, Pvals = [], []
for i in (0,1,3,4):
    presion = np.log(BM[i]["Presión"].values)
    pop, cov = curve_fit(bombeo2, BM[i].index.values, presion, sigma = error(BM[i]) , p0=[0.00156/4.5e-3, np.max(BM[i]["Presión"].values)], absolute_sigma=True)
    Parametros.append(pop)
    Errores.append(np.sqrt(np.diag(cov)))
    chi, pv, nu = chi2_pvalor(BM[i].index.values, presion, error(BM[i]), bombeo2(BM[i].index.values, *pop), 2)
    Chis.append(chi/nu)
    Pvals.append(pv)
    # residuos(bombeo, pop, BM[i].index.values, BM[i]["Presión"].values, error(BM[i]), grafico = True)

plt.show(block=True)

for i in range(len(Parametros)):
    ind = (0,1,3,4)
    presion = np.log(BM[ind[i]]["Presión"].values)
    plt.figure(figsize=(6, 4))
    plt.title(f"BM{ind[i]}")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Presión [Torr]")
    plt.fill_between(BM[ind[i]].index, presion - error(BM[ind[i]]), presion + error(BM[ind[i]]), alpha=0.3)
    plt.plot(BM[ind[i]].index, presion,".k", label="Mediciones BM")
    ejex = np.linspace(0, np.max(BM[ind[i]].index), 10000)
    plt.plot(ejex, bombeo2(ejex, *Parametros[i]), "r", label="Ajuste")
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    #plt.legend()

plt.show(block=True)