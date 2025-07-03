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

def perdidas(t,CV,QV,p0,A,B): # CV = C/V ; QV = Q/V ; PE = 750 ; c = fuga  1 - c = desgase
    return A*fuga(t,CV,p0) + B*desgase(t,QV,p0) 

def error(df):
    p = np.array(df["Presión"].values)
    std = []
    for y in p:                  # error sensor 
        std.append(0.0075*y)
        # if y > 7.5e-4:
        #     std.append(0.15*y)
        # elif y > 75:
        #     std.append(0.05*y)
        # else:
        #     std.append(0.30*y)

    for i in range(len(std)-1):  # error temporal
        a = (p[i+1] - p[i])/np.sqrt(12)
        # if a > std[i]:
        std[i] = std[i] + a

    return np.array(std)



Parametros, Errores = [], []
Chis, Pvals = [], []
for i in (0,1,2):
    try:
        funciones = [fuga, desgase, perdidas]
        p0 = [[5e-5,F["Presión"][0]],[3e-4,F["Presión"][0]],[5e-5,1e-4,F["Presión"][0],1,0]]
        bounds = [((0,np.inf),(0,np.inf)),((0,np.inf),(0,np.inf)),((0,np.inf),(0,np.inf),(0,np.inf),(0,1))]
        pop, cov = curve_fit(funciones[i], F.index.values, F["Presión"].values, sigma = error(F) , p0=p0[i], absolute_sigma=True) #, bounds=bounds[i])
        Parametros.append(pop)
        Errores.append(np.sqrt(np.diag(cov)))
        chi, pv, nu = chi2_pvalor(F.index.values, F["Presión"].values, error(F), funciones[i](F.index.values, *pop), 2)
        Chis.append(chi/nu)
        Pvals.append(pv)
        # residuos(funciones[i], pop, F.index.values, F["Presión"].values, error(F), grafico = True)
    except:
        print("Error en ajuste", funciones[i])
        if i in (0,1):
            Parametros.append([0,0])
            Errores.append([0,0])
        else: 
            Parametros.append([0,0,0,0])
            Errores.append([0,0,0,0])
        Chis.append(0)
        Pvals.append(0)
plt.show(block=True)

# resultados
for i in (0,1,2): 
    print(funciones[i].__name__)
    print("pvalor: ", Pvals[i], "Chi: ", Chis[i])
    if i == 0:
        print("C/V: ", Parametros[i][0], "±", Errores[i][0], "p0: ", Parametros[i][1], "±", Errores[i][1])
    if i == 1:
        print("Q/V: ", Parametros[i][0], "±", Errores[i][0], "p0: ", Parametros[i][1], "±", Errores[i][1])
    if i == 2:
        print("C/V: ", Parametros[i][0], "±", Errores[i][0], "Q/V: ", Parametros[i][1], "±", Errores[i][1], "p0: ", Parametros[i][2], "±", Errores[i][2], "A: ", Parametros[i][3], "±", Errores[i][3], "B: ", Parametros[i][4], "±", Errores[i][4])
print()

plt.figure(figsize=(8, 6))
plt.title("F (pcte BM)")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.fill_between(F.index, F["Presión"] - error(F), F["Presión"] + error(F), alpha=0.3)
plt.plot(F.index, F["Presión"],".", label="Mediciones F")
for i in (0,1,2):
    plt.plot(F.index, funciones[i](F.index.values, *Parametros[i]), label=f"Ajuste {funciones[i]}")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.legend()

# plt.figure(figsize=(8, 6))
# plt.title("pcte BD 4")
# plt.xlabel("Tiempo [s]")
# plt.ylabel("Presión [Torr]")
# plt.fill_between(pcteBD[3].index, pcteBD[3]["Presión"] - error(pcteBD[3]), pcteBD[3]["Presión"] + error(pcteBD[3]), alpha=0.3)
# plt.plot(pcteBD[3].index, pcteBD[3]["Presión"],".", label="Medición pcteBD4")
# f = ["fuga", "desgase", "perdidas"]
# for i in (0,1,2):
#     plt.plot(pcteBD[3].index, funciones[i](pcteBD[3].index, *Parametros[i]), label=f"Ajuste {f[i]}")
# plt.grid(color="gray", linestyle="-", linewidth=0.5)
# plt.legend()

plt.show(block=True)