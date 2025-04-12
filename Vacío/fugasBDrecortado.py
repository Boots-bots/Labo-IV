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
        std.append(0.07*y)
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

# recorte 1.7e-5

def cortar_por_presion(df, umbral=1.5e-5):
    """
    Elimina todas las filas desde el primer valor en la columna 'Presión'
    que sea mayor al umbral (incluido).
    """
    idx = df[df["Presión"] > umbral].index
    if not idx.empty:
        corte = idx[0]  # Primer índice donde se supera el umbral
        return df.loc[:corte-1].reset_index(drop=True)
    else:
        # Si nunca se supera el umbral, se devuelve el DataFrame completo
        return df.reset_index(drop=True)
    
for i in range(len(fugaBD)):
    fugaBD[i] = cortar_por_presion(fugaBD[i], umbral = 1.5e-5)
fugaBD[2] = cortar_por_presion(fugaBD[2], umbral = 1.25e-5)
fugaBD[1] = cortar_por_presion(fugaBD[1], umbral = 1.2e-5)


## ajustes 
Parametros, Errores = [], []
Chis, Pvals = [], []
for i in (0,1,2,3,4):
    if i == 3:
        Chis.append(0)
        Pvals.append(0)
        Parametros.append([0, 0, 0])
        Errores.append([0, 0, 0])
        continue
    else:
        pop, cov = curve_fit(fuga, fugaBD[i].index.values, fugaBD[i]["Presión"].values, sigma = error(fugaBD[i]) , p0=[2e-6, fugaBD[i]["Presión"].loc[0]], absolute_sigma=True)
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
    print("C/V: ", Parametros[i][0], "±", Errores[i][0],"p0: ", Parametros[i][1], "±", Errores[i][1])


color = ("b","orange","g","r","k")
ejex = np.linspace(0, 1e10, 1000)

for i in (0,1,2,4):
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
for i in (0,1,2,4):
    ejex = np.linspace(np.min(fugaBD[i].index), np.max(fugaBD[i].index), 10000)
    plt.fill_between(fugaBD[i].index, fugaBD[i]["Presión"] - error(fugaBD[i]), fugaBD[i]["Presión"] + error(fugaBD[i]), alpha=0.3)
    plt.plot(fugaBD[i].index, fugaBD[i]["Presión"], ".", color = color[i], label=f"Mediciones fugaBD{i+1}")
    plt.plot(ejex, fuga(ejex, *Parametros[i]), color = color[i])
# plt.ylim(np.min(fugaBD[i]["Presión"])*0.8, np.max(fugaBD[i]["Presión"])*1.2)
plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 

plt.show(block=True)