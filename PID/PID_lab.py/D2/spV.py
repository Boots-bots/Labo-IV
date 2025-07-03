# Imports
import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt
from collections import deque 
# import pyswarms as ps
import pandas as pd
import os
import cv2 #esto conecta la camara al programa
import serial
import time
from datetime import datetime
import serial.tools.list_ports

# setpoint variable 

def stair_function(t, step_size=10, step_value=50):
    """Saltos step_value cada step_size segundos."""
    return step_value * np.floor_divide(t, step_size)  

from scipy.signal import sawtooth
def sawSleepTooth(t, sleep=5, largo=20):
    """Onda diente de sierra que arranca después de `sleep` segundos."""
    if t < sleep:
        return 80
    else:
        # Rango: [80, 400]
        return (sawtooth((t - sleep) * 2 * np.pi / (largo - sleep), width=0.5) + 1) * 80 + 80

def senoidal(t, periodo=10, ofs = 250, amp = 40, fase = 0):
    """Senoidal de amplitud 350."""
    return (amp*np.sin(2*np.pi*t/periodo - fase) + ofs)

def rampa(t, velocidad=20, maximo=240):
    """Lineal con el tiempo, hasta un valor máximo."""
    return min(t * velocidad, maximo)

def exponencial1(t, tau=7.25, amplitud=255):
    """Exponencial hacia `amplitud`, con constante de tiempo `tau`."""
    return amplitud*(1 - np.exp(-t / tau))

def exponencial2(t, tau=7.25, amplitud=0.05):
    """Exponencial"""
    return amplitud*np.exp(t / tau)  


# xs = np.linspace(0, 60, 1000)  # 1000 puntos entre 0 y 60 segundos
# plt.figure()
# for x in xs:
#     plt.plot(x, stair_function(x),".b")
#     plt.plot(x, sawSleepTooth(x),".r")
#     plt.plot(x, senoidal(x),".g")
#     plt.plot(x, rampa(x),".m")
#     plt.plot(x, exponencial1(x),".y")
#     plt.plot(x, exponencial2(x),".k")
# plt.title("Funciones de Setpoint")
# plt.xlabel("Tiempo [s]")
# plt.ylabel("Setpoint [u.a.]")
# plt.grid()
# plt.show(block=True)

exit()

#%% Eval med PID

def evaluar_pid(K, duracion=60, setpoint=300, spf = None, guardar_csv=False, plot = False, save_folder="C:/Users/publico/Desktop/Grupo_1/Med/", **spf_kwargs): # 3.0 # al fondo todos los parametros de spf
    Kp, Ki, Kd = K              # ≈ 66.5 s por evaluación     # va el nombre directo de la función 

    integrador = 0
    tiempo_anterior = None
    ISE = 0

    tiempos, posiciones, errores = [], [], []
    P_terms, I_terms, D_terms, señales = [], [], [], []  
    setpoints = []

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

        # Calcular setpoint en cada instante
        setpoint_actual = setpoint if spf is None else spf(tiempo_actual, **spf_kwargs)

        error = setpoint_actual - pos
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
        setpoints.append(setpoint_actual)
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
        plt.plot(tiempos, setpoints, color="red")
        plt.plot(tiempos, posiciones, ".-")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Posición [u.a.]")
        plt.grid()

    for name, data in zip(["Proporcional", "Integrativo", "Derivativo"], [P_terms, I_terms, D_terms]):
        plt.figure()
        plt.title(f"Término {name}")
        plt.plot(tiempos, data, ".-")
        plt.xlabel("Tiempo [s]")
        plt.ylabel(f"Valor {name[0]}")
        plt.grid()

    if guardar_csv:
        # Crear DataFrame
        df = pd.DataFrame({
            "tiempo": tiempos,
            "posicion": posiciones,
            "setpoint": setpoints,
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
