import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from settings.imports import*
from settings.estética import*
from settings.ajustes import*
from settings.propagación import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

P = []
for i in (0,1,2,3,4,5):
    P.append(pd.read_csv(folder + "calor/" + f"P{i}.csv"))  # {"tiempo":tiempoP, "presion":presion}
R = []
for i in (0,1,2,3,4,5):
    R.append(pd.read_csv(folder + "calor/" + f"R{i}.csv"))    # {"tiempo":tiempoR, "resistencia":resistencia, "temperatura":temperatura}

tamb = np.mean(R[0]["temperatura"].values)
tambstd = np.std(R[0]["temperatura"].values)
tambp = np.mean(R[1]["temperatura"].values)
tambpstd = np.std(R[1]["temperatura"].values)

def error_presion(df):
    p = np.array(df["presion"].values)
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

def NTC_res2temp_poli(R): #en Ohm
   a,b,c,d,e,f = [ 8.30898289e+02, -4.43056704e+02,  1.16417971e+02, -1.87119140e+01,
      1.63900559e+00, -5.96756860e-02]
   R = np.array(R)
   logR = np.log(R)
   return a + b*logR + c*logR**2 + d*logR**3 + e*logR**4 + f*logR**5

def prop_Ntc(R,stdR):
    a,b,c,d,e,f = [ 8.30898289e+02, -4.43056704e+02,  1.16417971e+02, -1.87119140e+01, 1.63900559e+00, -5.96756860e-02]
    numerador = 2*c + 6*d*np.log10(R) + (12*e*np.log10(R)**2) + (20*f*np.log10(R)**3) - np.log(10)*b - 2*c*np.log(R) - (3*np.log(10)*d*np.log10(R)**2) - (4*np.log(10)*e*np.log10(R)**3) - (5*np.log(10)*f*np.log10(R)**4)
    denominador = (np.log(10)**2)*R**2
    f = (numerador/denominador)
    return f*stdR

def error_mult(L,x,n,Dms):
    return (x*L + n*Dms)

dms = 1000
x = 0.008
n = 1

stdR = [error_mult(R[i]["resistencia"].values, x, n, dms) for i in range(len(R))]
stdT = [prop_Ntc(R[i]["resistencia"].values, stdR[i]) for i in range(len(R))]

stdT = [(stdT[i] + 0.001*R[i]["temperatura"].values) for i in range(len(R))]

P0 = [np.mean(P[i]["presion"].values) for i in range(len(P))]

def T(t, tau, y):
    return (P0[4]/y)*(1 - np.exp(-t/tau)) # A = P0/y = 2*P0*tau/a*Lc

def Tbaj(t, Te , tau):
    return Te*np.exp(-t/tau) + 303  # Te = P0/y = 2*P0*tau/a*Lc   


gamma = 4*5.670374419e-8 * 0.3 * (30+273)**3 # a(4*sgm*eps*Tamb**3 + h) sgm = 5.670374419e-8 W/m^2K^4  
A = P0[4]/(0.385*0.5) # 2*P0/a*Lc #a = 2

Rk = []
for i in range(len(R)):
    Ri = R[i]+273 # R = R + 273.15 en K
    Rk.append(Ri)

R = Rk

pop, cov = curve_fit(T, R[4]["tiempo"].values, R[4]["temperatura"].values, sigma = stdT[4] , p0=[2000,gamma], absolute_sigma=True)
popstd = (np.sqrt(np.diag(cov)))
chi, pv, nu = chi2_pvalor(R[4]["tiempo"].values, R[4]["temperatura"].values, stdT[4], T(R[4]["tiempo"].values, *pop), 3)
chi = chi/nu
# residuos(T, pop, R[4]["tiempo"].values, R[4]["temperatura"].values, stdT[4], grafico = True)


print("R4")
print("pvalor: ", pv, "Chi: ", chi)
print("tauR: ", pop[0], "±", popstd[0],"A: ", pop[1], "±", popstd[1])

ejex = np.linspace(np.min(R[4]["tiempo"].values), np.max(R[4]["tiempo"].values), 10000)

plt.figure()
plt.plot(R[4]["tiempo"], R[4]["temperatura"], ".", label=f"Med:{4}")
plt.fill_between(R[4]["tiempo"], R[4]["temperatura"] - stdT[4], R[4]["temperatura"] + stdT[4], alpha=0.3)
plt.plot(ejex, T(ejex, *pop), label="Ajuste", color="red")
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.xlabel("Tiempo [s]")
plt.ylabel("Temperatura [K]")
plt.title(f"T{i}")
plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 

plt.figure()
plt.plot(P[4]["tiempo"], P[4]["presion"], ".", label=F"Med:{4}")
plt.fill_between(P[4]["tiempo"], P[4]["presion"] - error_presion(P[4]), P[4]["presion"] + error_presion(P[4]), alpha=0.3)
plt.grid(color="gray", linestyle="-", linewidth=0.5)
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.title(f"P{i}")
plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 

plt.show(block=True)

exit()

for i in (0,1,2,3,4,5):
    plt.figure()
    plt.plot(P[i]["tiempo"], P[i]["presion"], ".", label=F"Med:{i}")
    plt.fill_between(P[i]["tiempo"], P[i]["presion"] - error_presion(P[i]), P[i]["presion"] + error_presion(P[i]), alpha=0.3)
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Presión [Torr]")
    plt.title(f"P{i}")
    plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 

    plt.figure()
    plt.plot(R[i]["tiempo"], R[i]["temperatura"], ".", label=f"Med:{i}")
    plt.fill_between(R[i]["tiempo"], R[i]["temperatura"] - stdT[i], R[i]["temperatura"] + stdT[i], alpha=0.3)
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Temperatura [°C]")
    plt.title(f"T{i}")
    plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 

    plt.figure()
    plt.plot(R[i]["tiempo"], R[i]["resistencia"], ".", label=f"Med:{i}")
    plt.fill_between(R[i]["tiempo"], R[i]["resistencia"] - stdR[i], R[i]["resistencia"] + stdR[i], alpha=0.3)
    plt.grid(color="gray", linestyle="-", linewidth=0.5)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Resistencia [Ω]")
    plt.title(f"R{i}")
    plt.legend(loc = "lower right", facecolor='white', framealpha=0.5, fontsize = 12, edgecolor='grey') 

plt.show(block=True)

exit()
