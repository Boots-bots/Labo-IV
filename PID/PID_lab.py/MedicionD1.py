# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 08:37:06 2025

@author: Publico
"""
# Imports
import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
import pyswarms as ps
import pandas as pd
import os
import cv2 #esto conecta la camara al programa
import serial
import time
from datetime import datetime
import serial.tools.list_ports
Kin = (0.1125, 0.0001875, 0.5)

#%% Enchufe 
ports = serial.tools.list_ports.comports()

# Print info about each port
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")

#%% definiciones de funciones

def trackTemplate(vs, template, limites):
    '''
    Parameters
    ----------
    vs : cámara
        DESCRIPTION.
    template : string
        Path de la imagen template.
    limites : list
        Extremos para recortar el tubo en la imagen.

    Returns
    -------
    int
        La posición (en px) del extremo superior del template detectado.

    '''
    # Toma foto. Si no puede devuelve None
    im = vs.read()[1]
    if im is None:
        return None

    # Corte zona del tubo y pasado a escala de grises y a enteros.
    min_x, max_x, min_y, max_y = limites
    im = im[min_y:max_y, min_x:max_x, :]
    #cv2.imshow('',im)
    im = np.mean(im, axis=2)
    im = np.asarray(im, np.uint8)

    # Lee el template y lo trackea. Devuelve como posición la esquina superior izquierda.
    template = cv2.imread(template)

    if template is None:
        raise ValueError(f"No se pudo cargar la imagen del template desde {template}")
    template = np.mean(template, axis=2)
    template = np.asarray(template, np.uint8)
    res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF)
    top_left = cv2.minMaxLoc(res)[3]

    return top_left[0]


#%% Inicialización de la cámara
vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#%% Inicialización comunicación Arduino (VER COM) Inicializarlo solo una vez, no lo corran mas despues de eso
arduino = serial.Serial(port='COM13', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.05, xonxoff=0, rtscts=0)
time.sleep(2)

#%% Guardado imagen del vaso, en escala de grises
im = vs.read()[1]
im = np.mean(im, axis=2)
imsave("completa.png", im, cmap='gray')
temp = cv2.imread('completa.png')
cv2.imshow("",temp)

# Guardado imagen recortada (tubo/template), en escala de grises
im = vs.read()[1]
limites_vasito=[6,98, 204, 280]
limites_tubo=[0,580,200,280]
min_x, max_x, min_y, max_y = limites_vasito
im = im[min_y:max_y, min_x:max_x, :]
im = np.mean(im, axis=2)
imsave('vasito.png', im, cmap='gray')
temp = cv2.imread('vasito.png')
time.sleep(1)
cv2.imshow("",temp)

# Ubicación imagen template
template = 'vasito.png'
cv2.imshow("",temp)

#%% Prueba ventilador
arduino.write(bytes(f'a0\n', 'utf-8'))
#time.sleep(15)
arduino.write(bytes(f'a100\n', 'utf-8')) # 152 ± 5 estabilidad
#%% prueba camara
duracion = 100

tiempo = []
posicion = []
t0 = time.time()

while time.time() - t0 < duracion:
    arduino.write(bytes(f'a153\n', 'utf-8'))
    tiempo.append(time.time() - t0)
    pos = trackTemplate(vs, template, limites_tubo)
    if pos is None:
        print("No se pudo detectar la posición")
        continue
    posicion.append(pos)
    if pos > 250:
        arduino.write(bytes(f'a115\n', 'utf-8'))
    if pos < 100 :
        arduino.write(bytes(f'a190\n', 'utf-8'))
    if pos < 5:
        arduino.write(bytes(f'a200\n', 'utf-8'))

print("Finich")

# plot
plt.figure()
plt.plot(tiempo, posicion,".-")
plt.xlabel("Tiempo [s]")

#%% conversores 
# comversor pot a %
def por(x):
    return x*100/255

# conversor de pixeles a cm
L = 72 #cm longitud del tubo ±1
resolución = 590 # pixeles en el eje x
def pixacm(x):
  return x*L/resolución

#%% Save Foler
save_folder = "C:/Users/publico/Desktop/Grupo_1/Med/"
#%% Cuadrado
save_folder = "C:/Users/publico/Desktop/Grupo_1/Med/"

arduino.write(bytes(f'a100\n', 'utf-8'))
# cuadrado
duracion = 30  # 30 255
I = int(170)

tiempo = []
posicion = []
señal = []
t0 = time.time()

while time.time() - t0 < duracion:
    if time.time()-t0 > 5:  ######
        arduino.write(bytes(f'a{I}\n', 'utf-8'))
        señal.append(I)
    else:
        arduino.write(bytes(f'a0\n', 'utf-8'))
        señal.append(0)
    tiempo.append(time.time() - t0)
    pos = trackTemplate(vs, template, limites_tubo)
    if pos is None:
        print("No se pudo detectar la posición")
        continue
    posicion.append(pos)

print("Finich")

# plot

ax1 = plt.subplot(211)
ax1.plot(tiempo, posicion, ".-")
ax2 = plt.subplot(212, sharex=ax1)
ax1.set_ylabel("Posición")
ax2.plot(tiempo, señal, "r-")
ax2.set_ylabel('Señal')
ax2.set_xlabel('tiempo(s)')

plt.show()

# Guardado
df = pd.DataFrame({
            "tiempo": tiempo,
            "posicion": posicion,
            "señal": señal,
        })

os.makedirs(save_folder, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_archivo = f"cuadrada-I_{I}_{timestamp}.csv"
df.to_csv(save_folder + nombre_archivo, index=False, header=True)

#%% Lineal

save_folder = "C:/Users/publico/Desktop/Grupo_1/Med/"
duracion = 60  
m = 2

tiempo = [0,0]
posicion = [0,0]
señal = [0,0]
t0 = time.time()

I=0
while time.time() - t0 < duracion:
    while I <= 255:
        pos = trackTemplate(vs, template, limites_tubo)
        if pos is None:
            print("No se pudo detectar la posición")
            continue
        tiempo.append(time.time() - t0)
        posicion.append(pos)
        señal.append(I)
        time.sleep(0.5)
        I += m  
        arduino.write(bytes(f'a{I}\n', 'utf-8'))
    arduino.write(bytes(f'a255\n', 'utf-8'))


print("Finich")

# plot

ax1 = plt.subplot(211)
ax1.plot(tiempo, posicion, ".-")
ax2 = plt.subplot(212, sharex=ax1)
ax1.set_ylabel("Posición")
ax2.plot(tiempo, señal, "r-")
ax2.set_ylabel('Señal')
ax2.set_xlabel('tiempo(s)')

plt.show()

df = pd.DataFrame({
            "tiempo": tiempo,
            "posicion": posicion,
            "señal": señal,
        })

os.makedirs(save_folder, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_archivo = f"lineal-{m}_{timestamp}.csv"
df.to_csv(save_folder + nombre_archivo, index=False, header=True)

#%% Eval med PID

def evaluar_pid(K, duracion=60, setpoint=300, guardar_csv=False, plot = False, save_folder="C:/Users/publico/Desktop/Grupo_1/Med/"):
    Kp, Ki, Kd = K              # ≈ 66.5 s por evaluación

    integrador = 0
    error_anterior = 0
    tiempo_anterior = None
    ISE = 0

    tiempos, posiciones, errores = [], [], []
    P_terms, I_terms, D_terms, señales = [], [], [], []

    errores_recientes = [] ###
    i = 0

    # Apagar ventiladores antes de comenzar
    arduino.write(bytes(f'a153\n', 'utf-8'))
    time.sleep(2)

    t0 = time.time()

    while time.time() - t0 < duracion:
        tiempo_actual = time.time() - t0
        pos = trackTemplate(vs, template, limites_tubo)
        if pos is None:
            continue

        error = setpoint - pos
        errores_recientes.append(error)  ####
        
        dt = tiempo_actual - tiempo_anterior if tiempo_anterior else 0 
        tiempo_anterior = tiempo_actual

        # PID
        P = Kp * error
        
       # integrador += error * dt
        integrador = sum(errores_recientes[(i-4):])  ###
        i += 1
        
        #integrador = max(min(integrador, 1000), -1000)  # regula el windup (saturación)
        I = Ki * 0.03 * integrador
        if (len(posiciones) >= 3):
            derivativo = (errores_recientes[-1] - errores_recientes[-3]) / (dt*2)
        else:
            # Manejar el caso en que no haya suficientes datos en 'posicion'
            derivativo = 0
        
        D = Kd * derivativo
        
        error_anterior = error

        control_signal = P + I + D
        control_signal = max(0, min(255, control_signal))
        arduino.write(bytes(f'a{int(control_signal)}\n', 'utf-8'))

        # ISE
        ISE += error**2 * dt

        # Guardar datos
        tiempos.append(tiempo_actual)
        posiciones.append(pos)
        errores.append(error**2 * dt)
        P_terms.append(P)
        I_terms.append(I)
        D_terms.append(D)
        señales.append(control_signal)

    # Apagar
    arduino.write(bytes(f'a120\n', 'utf-8'))
    time.sleep(3)
    arduino.write(bytes(f'a0\n', 'utf-8'))

    if plot:
        plt.figure()
        plt.title("Posición")
        plt.axhline(setpoint, linestyle="--")
        plt.plot(tiempos, posiciones, ".-")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Posición [u.a.]")
        plt.grid()

        plt.figure()
        plt.title("Término Proporcional")
        plt.plot(tiempos, P_terms, ".-")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Valor P")
        plt.grid()

        plt.figure()
        plt.title("Término Integrativo")
        plt.plot(tiempos, I_terms, ".-")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Valor I")
        plt.grid()

        plt.figure()
        plt.title("Término Derivativo")
        plt.plot(tiempos, D_terms, ".-")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Valor D")
        plt.grid()

    if guardar_csv:
        # Crear DataFrame
        df = pd.DataFrame({
            "tiempo": tiempos,
            "posicion": posiciones,
            "error": errores,
            "P": P_terms,
            "I": I_terms,
            "D": D_terms,
            "control": señales,
            "Kp": [Kp] * len(tiempos),
            "Ki": [Ki] * len(tiempos),
            "Kd": [Kd] * len(tiempos),
            "ISE": [ISE] * len(tiempos)
        })

        os.makedirs(save_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Kp{Kp:.2f}_Ki{Ki:.2f}_Kd{Kd:.2f}_Set{setpoint}_ISE{ISE:.2f}_{timestamp}.csv"
        df.to_csv(os.path.join(save_folder, filename), index=False, header=True)

    return ISE


#%% Venti
arduino.write(bytes(f'a0\n', 'utf-8'))

#%% Mediciòn
#kc = 3.5
#Tc = 4.7 
#Kz = (0.6*kc, 1.2*kc/Tc, 3*kc*Tc/40 ) # Ziegler-Nichols 

kc = 0.25
Kp = kc*10   # 2.5
Ki= 25*kc/8  # 0.78 
Kd = 7*kc    # 1.75

K = (2*Kp,Ki*30,3*Kd)

#for i in range(5):
evaluar_pid(K, duracion = 30, setpoint = 300, guardar_csv = True, plot = True)

#%% Calculadora de tiempo
n_particles = 5
iters = 10
tmed = 20
print(f"Tiempo total estimado: {n_particles*iters*tmed/60:.2f} minutos")

#%%  PSO 
sp = 300

# Definir límites (mismos que usabas en DE)
bounds = (np.array([10, 17, 6]), np.array([20, 40, 20]))  # Kp, Ki, Kd
# Función que PSO acepta: recibe una matriz de forma (n_partículas, 3)
def objective_function(K):
    return np.array([evaluar_pid(k, duracion=20, setpoint=sp, guardar_csv=True) for k in K])

# Parámetros del PSO
options = {'c1': 1.2, 'c2': 1.4, 'w': 0.7}
n_particles = 5
iters = 10

# Inicializar optimizador
optimizer = ps.single.GlobalBestPSO(
    n_particles=n_particles,
    dimensions=3,
    options=options,
    bounds=bounds
)

# Ejecutar optimización
cost, pos = optimizer.optimize(objective_function, iters=iters)

print("\n✅ Optimización con PSO finalizada:")
print(f"Kp = {pos[0]:.4f}")
print(f"Ki = {pos[1]:.6f}")
print(f"Kd = {pos[2]:.4f}")
print(f"ISE mínimo = {cost:.4f}")

#%%
# Evaluar con los mejores parámetros
ISE = evaluar_pid(pos, duracion=30, setpoint=sp, guardar_csv = True, plot=True)
print(f"\n✅ Simulación final con PID óptimo - ISE = {ISE:.4f}")
