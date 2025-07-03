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

# segun el apunte, lo unico que cambia es que agrega el b, y el D (con filtro)

def evaluar_pid(K, b = 1, N = 10, n= 5, duracion=60, setpoint=300, spf = None, guardar_csv=False, plot = False, save_folder="C:/Users/publico/Desktop/Grupo_1/Med/", **spf_kwargs): # 3.0 # al fondo todos los parametros de spf
                           # ≈ 66.5 s por evaluación     # va el nombre directo de la función 
    # Kp = K ; Ki = K/ti ; Kd = K*td ; b = 1, c = 0
    # N filtro derivativo de primer orden
    # n antiwindup casero
    Kp, Ki, Kd = K
    ti = Kp / Ki if Ki != 0 else 0
    td = Kd / Kp if Kp != 0 else 0
    c = 0  

    tiempo_anterior = None
    ISE = 0

    errores_recientes = deque(maxlen=n)  # Mantener los últimos 5 
    dt_recientes = deque(maxlen=n)

    tiempos, posiciones, errores = [], [], []
    P_terms, I_terms, D_terms, señales = [0], [0], [0], []  
    setpoints = []

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

        # PID 2dof
        P = Kp * (b * setpoint_actual - pos)
        
        I = Ki* sum(e * t for e, t in zip(errores_recientes, dt_recientes))  ###        

        D =  td/(td + N * dt) * (D_terms[-1] - Kp*N*(pos - setpoints[-1]))  # Derivativo modificado

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
            "b": [b] * len(tiempos),
            "c": [c] * len(tiempos),
            "ISE": [ISE] * len(tiempos)
        })

        os.makedirs(save_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Kp{Kp:.2f}_Ki{Ki:.2f}_Kd{Kd:.2f}_b{b:.2f}_c{c:.2f}_Set{setpoint}_ISE{ISE:.2f}_{timestamp}.csv"
        df.to_csv(os.path.join(save_folder, filename), index=False, header=True)

    return ISE
