# Imports
import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt
from collections import deque 
import pyswarms as ps
import pandas as pd
import os
import cv2 #esto conecta la camara al programa
import serial
import time
from datetime import datetime
import serial.tools.list_ports

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
IMG = vs.read()[1]
limites_vasito=[6,98,204,280]
limites_tubo=[0,580,200,280]

min_x, max_x, min_y, max_y = limites_vasito
im = IMG[min_y:max_y, min_x:max_x, :]
im = np.mean(im, axis=2)

minT_x, maxT_x, minT_y, maxT_y = limites_tubo
imT = IMG[minT_y:maxT_y, minT_x:maxT_x, :]
imT = np.mean(imT, axis=2)

imsave('vasito.png', im, cmap='gray')
temp = cv2.imread('vasito.png')

imsave('tubo.png', imT, cmap='gray')
tubo = cv2.imread('tubo.png')

time.sleep(1)
# Ubicación imagen template
template = 'vasito.png'
cv2.imshow("",temp)
cv2.imshow("",tubo) 

#%% Prueba ventilador
arduino.write(bytes(f'a0\n', 'utf-8'))
#time.sleep(15)
arduino.write(bytes(f'a100\n', 'utf-8')) # 152 ± 5 estabilidad

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

#%% Eval med PID

def evaluar_pid(K, duracion=60, setpoint=300, guardar_csv=False, plot = False, save_folder="C:/Users/publico/Desktop/Grupo_1/Med/"):  # 2.0
    Kp, Ki, Kd = K              # ≈ 66.5 s por evaluación

    integrador = 0
    tiempo_anterior = None
    ISE = 0

    tiempos, posiciones, errores = [], [], []
    P_terms, I_terms, D_terms, señales = [], [], [], []  

    n = 5 # windup casero 
    errores_recientes = deque(maxlen=n)  # Mantener los últimos 5 
    dt_recientes = deque(maxlen=n)

    # Setear ventilador nulo
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
        dt_recientes.append(dt)
        tiempo_anterior = tiempo_actual

        # PID
        P = Kp * error
         
        integrador = sum(e * t for e, t in zip(errores_recientes, dt_recientes))  ###
        I = Ki * integrador

        if (len(posiciones) >= 3):
            derivativo = (errores_recientes[-1] - errores_recientes[-3]) / (dt_recientes[-1]+dt_recientes[-2])   # filtro antiruido casero 2pasos
        else:
            # Manejar el caso en que no haya suficientes datos en 'posicion'
            derivativo = 0
        
        D = Kd * derivativo
        
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
    time.sleep(1)

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

# Kz = (0.6*kc, 1.2*kc/Tc, 3*kc*Tc/40 ) # Ziegler-Nichols  #Tc = 4.7 
 
kc = 0.25    # kc = 3.5
Kp = kc*10   # 2.5
Ki= 25*kc/8  # 0.78 
Kd = 7*kc    # 1.75

K = (2*Kp,Ki*30,3*Kd)

#for i in range(5):
evaluar_pid(K, duracion = 30, setpoint = 300, guardar_csv = True, plot = True)

#%% Calculadora de tiempo
particulas = 5
iters = 10
tmed = 20
print(f"Tiempo total estimado: {particulas*iters*tmed/60:.2f} minutos")

#%%  PSO 
sp = 300
duracion = 20

bounds = (np.array([10, 17, 6]), np.array([20, 40, 20]))  # Kp, Ki, Kd

def objective_function(K):                # Función que PSO acepta: recibe una matriz de forma (n_partículas, 3)
    return np.array([evaluar_pid(k, duracion = duracion, setpoint = sp, guardar_csv = True, save_folder = "C:/Users/publico/Desktop/Grupo_1/Med/") for k in K])

# Parámetros del PSO
options = {'c1': 1, 'c2': 1.8, 'w': 0.5} # basado en la tesis, D1 {'c1': 1.2, 'c2': 1.4, 'w': 0.7}
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

#%% Evaluar con los mejores parámetros
ISE = evaluar_pid(pos, duracion=30, setpoint=sp, guardar_csv = True, plot=True)
print(f"\n✅ Resultado final con PID óptimo - ISE = {ISE:.4f}")
