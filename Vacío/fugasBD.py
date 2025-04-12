
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from settings.imports import*
from settings.estética import*
from settings.ajustes import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

fugaBD = []
for i in range(1, 6):
    fugaBD.append(pd.read_csv(folder+ "/Presión/" + f"fugaBD{i}.csv", index_col=["Tiempo"]))

fugaBD[4] = fugaBD[4].iloc[9:, :].reset_index(drop=True) # Eliminamos las primeras 9 mediciones de fugaBD5, pcte

def fuga(t,CV,p0,pe):
    "C conductancia de predidas"
    "V volumen de la cámara"
    "p0 presión inicial"
    "pe presión externa"
    return pe + (p0 - pe) * np.exp(-t*CV)  #CV = C/V PE = 750
 
def error(df):
    p = np.array(df["Presión"].values)
    std = []
    for y in p:                  # error sensor 
        # std.append(0.07*y)
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

## ajustes 
Parametros, Errores = [], []
Chis, Pvals = [], []
for i in range(len(fugaBD)):
    pop, cov = curve_fit(fuga, fugaBD[i].index.values, fugaBD[i]["Presión"].values, sigma = error(fugaBD[i]) , p0=[1e-3/0.01, fugaBD[i]["Presión"].loc[0], 4e-5], absolute_sigma=True)
    Parametros.append(pop)
    Errores.append(np.sqrt(np.diag(cov)))
    chi, pv, nu = chi2_pvalor(fugaBD[i].index.values, fugaBD[i]["Presión"].values, error(fugaBD[i]), fuga(fugaBD[i].index.values, *pop), 2)
    Chis.append(chi/nu)
    Pvals.append(pv)
    # residuos(fuga, pop, fugaBD[i].index.values, fugaBD[i]["Presión"].values, error(fugaBD[i]), grafico = True)

plt.show(block=True)


# resultados

for i in range(len(fugaBD)):
    print("fuga BM", i+1)
    print("pvalor: ", Pvals[i], "Chi: ", Chis[i])
    print("C/V: ", Parametros[i][0], "±", Errores[i][0],"p0: ", Parametros[i][1], "±", Errores[i][1], "pe: ", Parametros[i][2], "±", Errores[i][2])


color = ("b","orange","g","r","k")
ejex = np.linspace(0, 1e10, 1000)

for i in (0,1,2,3,4):
    ejex = np.linspace(np.min(fugaBD[i].index), np.max(fugaBD[i].index), 10000)
    plt.figure(figsize=(8, 6))
    # plt.title(f"fugas BD{i+1}")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Presión [Torr]")
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.fill_between(fugaBD[i].index, fugaBD[i]["Presión"] - error(fugaBD[i]), fugaBD[i]["Presión"] + error(fugaBD[i]), alpha=0.3)
    plt.plot(fugaBD[i].index, fugaBD[i]["Presión"], ".", color = color[i], label=f"Mediciones fugaBD{i+1}")
    plt.plot(ejex, fuga(ejex, *Parametros[i]), color = color[i])
    # plt.ylim(np.min(fugaBD[i]["Presión"])*0.8, np.max(fugaBD[i]["Presión"])*1.2)
    plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 



plt.figure(figsize=(8, 6))
# plt.title("fugas BD")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
for i in (0,1,2,3,4):
    ejex = np.linspace(np.min(fugaBD[i].index), np.max(fugaBD[i].index), 10000)
    plt.fill_between(fugaBD[i].index, fugaBD[i]["Presión"] - error(fugaBD[i]), fugaBD[i]["Presión"] + error(fugaBD[i]), alpha=0.3)
    plt.plot(fugaBD[i].index, fugaBD[i]["Presión"], ".", color = color[i], label=f"Mediciones fugaBD{i+1}")
    plt.plot(ejex, fuga(ejex, *Parametros[i]), color = color[i])
# plt.ylim(np.min(fugaBD[i]["Presión"])*0.8, np.max(fugaBD[i]["Presión"])*1.2)
plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 



plt.show(block=True)

exit()
# datos 

plt.figure(figsize=(8, 6))
# plt.title("fugas BD")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(fugaBD[0].index, fugaBD[0]["Presión"],".", label="fugaBD1")
plt.plot(fugaBD[1].index, fugaBD[1]["Presión"],".", label="fugaBD2")
plt.plot(fugaBD[2].index, fugaBD[2]["Presión"],".", label="fugaBD3")
plt.plot(fugaBD[3].index, fugaBD[3]["Presión"],".", label="fugaBD4") ##
plt.plot(fugaBD[4].index, fugaBD[4]["Presión"],".", label="fugaBD5")
plt.legend()

plt.figure(figsize=(8, 6))
plt.title("fuga BD 4")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.plot(fugaBD[3].index, fugaBD[3]["Presión"],".", label="fugaBD4")

plt.show(block=True)