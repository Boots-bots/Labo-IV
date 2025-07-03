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

# BD2 = pd.read_csv(folder+ "/Presión/" + f"BD2.csv", index_col=["Tiempo"])

def bombeo(t,SV,p0,pf):   #SV = S/V
    "S velocidad de bombeo"
    "V volumen de la cámara"
    "p0, pf presión inicial, final"
    return (p0 + pf) * np.exp(-t * SV) + pf

def bombeo2(t,b,a,c):   #
    return a*np.exp(-t*b) + c

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

# S = 5,6 m^3/h ; 0.00156 m^3/s
# V = 4.5 L = 4.5e-3 m^3

BM[0] = BM[0].iloc[6:].reset_index(drop=True)
BM[1] = BM[1].iloc[4:].reset_index(drop=True)
BM[3] = BM[3].iloc[1:].reset_index(drop=True)
BM[4] = BM[4].iloc[7:].reset_index(drop=True)

# BM[0] = BM[0].iloc[10:].reset_index(drop=True)
# BM[4] = BM[4].iloc[5:].reset_index(drop=True)

# BM[0] = BM[0].iloc[:-10].reset_index(drop=True)
# BM[1] = BM[1].iloc[:-10].reset_index(drop=True)
# BM[3] = BM[3].iloc[:-10].reset_index(drop=True)
# BM[4] = BM[4].iloc[:-10].reset_index(drop=True)


Parametros, Errores = [], []
Chis, Pvals = [], []
for i in (0,1,3,4):
    pop, cov = curve_fit(bombeo, BM[i].index.values, BM[i]["Presión"].values, sigma = error(BM[i]) , p0=[0.00156/4.5e-3, np.max(BM[i]["Presión"].values), np.min(BM[i]["Presión"].values)], absolute_sigma=True)
    Parametros.append(pop)
    Errores.append(np.sqrt(np.diag(cov)))
    chi, pv, nu = chi2_pvalor(BM[i].index.values, BM[i]["Presión"].values, error(BM[i]), bombeo(BM[i].index.values, *pop), 2)
    Chis.append(chi/nu)
    Pvals.append(pv)
    # residuos(bombeo, pop, BM[i].index.values, BM[i]["Presión"].values, error(BM[i]), grafico = True)

plt.show(block=True)

# resultados
print("Sm: ", 0.00156, "m^3/s")
for i in range(len(Parametros)):
    ind = (0,1,3,4)
    print("fuga BM", ind[i]+1)
    print("pvalor: ", Pvals[i], "Chi: ", Chis[i])
    print("S/V: ", Parametros[i][0], "±", Errores[i][0],"p0: ", Parametros[i][1], "±", Errores[i][1] ,"pf: ", Parametros[i][2], "±", Errores[i][2])
    print("S: ", Parametros[i][0]*4.5e-3, "±", Errores[i][0]*4.5e-3) # [m^3/s]

# for i in range(len(Parametros)):
#     ind = (0,1,3,4)
#     print("fuga BM", ind[i])
#     print("pvalor: ", Pvals[i], "Chi: ", Chis[i])
#     print("b = S/V: ", Parametros[i][0], "±", Errores[i][0],"a: ", Parametros[i][1], "±", Errores[i][1] ,"c: ", Parametros[i][2], "±", Errores[i][2])
#     print("S: ", Parametros[i][0]*4.5e-3, "±", Errores[i][0]*4.5e-3) # [m^3/s]

for i in range(len(Parametros)):
    
    label = (
    rf'$S/V = {Parametros[i][0]:.3f} \pm {Errores[i][0]:.3f}$' + '\n' +
    rf'$\chi^2 = {Chis[i]:.1f}$' + '\n' +
    rf'$pval = {Pvals[i]:.1f}$'
    )

    ind = (0,1,3,4)
    plt.figure(figsize=(6, 4))
    # plt.title(f"BM{ind[i]}")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Presión [Torr]")
    plt.fill_between(BM[ind[i]].index, BM[ind[i]]["Presión"] - error(BM[ind[i]]), BM[ind[i]]["Presión"] + error(BM[ind[i]]), alpha=0.3)
    plt.plot(BM[ind[i]].index, BM[ind[i]]["Presión"],".k", label="Medición BM")
    ejex = np.linspace(0, np.max(BM[ind[i]].index), 10000)
    plt.plot(ejex, bombeo(ejex, *Parametros[i]), "r", label = r'Ajuste: $(p_0 + p_f) \cdot e^{-t \cdot SV} + p_f$')
    plt.text(
    0.70, 0.75,
    label,
    transform=plt.gca().transAxes,  # Coordenadas relativas al gráfico (0 a 1)
    fontsize=10,
    verticalalignment='top',
    bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray")
    )
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.legend(loc = "upper right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey')

plt.show(block=True)