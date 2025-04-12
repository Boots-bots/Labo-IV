import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from settings.imports import*
from settings.estética import*
from settings.ajustes import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

fugaBM = []
for i in range(1, 6):
    fugaBM.append(pd.read_csv(folder+ "/Presión/" + f"fugaBM{i}.csv", index_col=["Tiempo"]))

def fuga(t,CV,p0):
    "C conductancia de predidas"
    "V volumen de la cámara"
    "p0 presión inicial"
    "pe presión externa"
    return 750 + (p0 - 750) * np.exp(-t*CV)  #CV = C/V PE = 750
 
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
for i in range(len(fugaBM)):
    pop, cov = curve_fit(fuga, fugaBM[i].index.values, fugaBM[i]["Presión"].values, sigma = error(fugaBM[i]) , p0=[3e-6, fugaBM[i]["Presión"][0]], absolute_sigma=True)
    Parametros.append(pop)
    Errores.append(np.sqrt(np.diag(cov)))
    chi, pv, nu = chi2_pvalor(fugaBM[i].index.values, fugaBM[i]["Presión"].values, error(fugaBM[i]), fuga(fugaBM[i].index.values, *pop), 2)
    Chis.append(chi/nu)
    Pvals.append(pv)
    # residuos(fuga, pop, fugaBM[i].index.values, fugaBM[i]["Presión"].values, error(fugaBM[i]), grafico = True)


plt.show(block=True)

# resultados
for i in range(len(fugaBM)):
    print("fuga BM", i+1)
    print("pvalor: ", Pvals[i], "Chi: ", Chis[i])
    print("C/V: ", Parametros[i][0], "±", Errores[i][0],"p0: ", Parametros[i][1], "±", Errores[i][1])

color = ("b","orange","g","k","r")

ejex = np.linspace(0, 1e7, 10000)

plt.figure(figsize=(8, 6))
# plt.title("fugas BM")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
for i in (0,1,2,4):
    ejex = np.linspace(np.min(fugaBM[i].index), np.max(fugaBM[i].index), 10000)
    plt.fill_between(fugaBM[i].index, fugaBM[i]["Presión"] - error(fugaBM[i]), fugaBM[i]["Presión"] + error(fugaBM[i]), alpha=0.3)
    plt.plot(fugaBM[i].index, fugaBM[i]["Presión"], ".", color = color[i], label=f"Mediciones fugaBM{i+1}")
    plt.plot(ejex, fuga(ejex, *Parametros[i]), color = color[i])
# plt.ylim(np.min(fugaBM[i]["Presión"])*0.8, np.max(fugaBM[i]["Presión"])*1.2)
plt.legend()


plt.show(block=True)
exit()
#datos

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

ejex = np.linspace(np.min(fugaBM[3].index), np.max(fugaBM[3].index), 10000)
plt.figure(figsize=(8, 6))
plt.title("fuga BM4")
plt.plot(fugaBM[3].index, fugaBM[3]["Presión"],".b", label="Mediciones fugaBM4")
plt.fill_between(fugaBM[3].index, fugaBM[3]["Presión"] - error(fugaBM[3]), fugaBM[3]["Presión"] + error(fugaBM[3]), alpha=0.3)
plt.plot(ejex, fuga(ejex, *Parametros[3]), "b", label="Ajuste fugaBM4")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.legend()
plt.ylim(np.min(fugaBM[3]["Presión"])*0.8, np.max(fugaBM[3]["Presión"])*1.2)

plt.show(block=True)