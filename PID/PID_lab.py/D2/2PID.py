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

# optimizacion de K2 
def set_pid(K, duracion=10, setpoint=300, tolerancia = 0.05, tiempo_estable = 3):  # en base a 2.0
    Kp, Ki, Kd = K             
    integrador = 0
    tiempo_en_tolerancia = 0
    tiempo_anterior = None
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
        if (len(errores_recientes) >= 3):
            derivativo = (errores_recientes[-1] - errores_recientes[-3]) / (dt_recientes[-1]+dt_recientes[-2])   # filtro antiruido casero 2pasos
        else:
            # Manejar el caso en que no haya suficientes datos en 'posicion'
            derivativo = 0
        D = Kd * derivativo
        control_signal = P + I + D
        control_signal = max(0, min(255, control_signal))
        arduino.write(bytes(f'a{int(control_signal)}\n', 'utf-8'))

        # Verificar si el error está dentro de la tolerancia
        if abs(error) < tolerancia * setpoint:
            tiempo_en_tolerancia += dt
        else:
            tiempo_en_tolerancia = 0

        if tiempo_en_tolerancia >= tiempo_estable:
            break
    # Apagar
    arduino.write(bytes(f'a153\n', 'utf-8'))
    time.sleep(1)

    return 

# ejecutar PSO sobre la funccion evaluar, en bucle con la de seteo (asegurarse que la de seteo funcione bien)

###########################################################
#%% Doble PID
def controlador_2pid(K1,K2, duracion=60, tolerancia=0.05, setpoint=300, spf = None, guardar_csv=False, plot = False, save_folder="C:/Users/publico/Desktop/Grupo_1/Med/", **spf_kwargs): # en base a 3.0
                                              # ≈ 66.5 s por evaluación     # va el nombre directo de la función   # K2 es para estabilidad
    Kp1, Ki1, Kd1 = K1
    Kp2, Ki2, Kd2 = K2       

    integrador = 0
    tiempo_anterior = None
    ISE = 0

    tiempos, posiciones, errores = [], [], []
    P_terms, I_terms, D_terms, señales = [], [], [], []  
    setpoints = []
    controladores = [] # 1: PID1, 2: PID2

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
        if error < tolerancia*setpoint_actual:  # tolerancia
            controlador = 2
            Kp = Kp2
            Ki = Ki2
            Kd = Kd2
        else:
            controlador = 1
            Kp = Kp1
            Ki = Ki1
            Kd = Kd1

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
        controladores.append(controlador)
        señales.append(control_signal)

    # Apagar
    arduino.write(bytes(f'a120\n', 'utf-8'))
    time.sleep(3)
    arduino.write(bytes(f'a0\n', 'utf-8'))
    time.sleep(1)

    if plot:
        plt.figure()
        plt.title("Posición")
        plt.fill_between(tiempos, np.array(setpoints)-tolerancia*np.array(setpoints), np.array(setpoints)+tolerancia*np.array(setpoints), color="red", alpha=0.2, label="Tolerancia")
        plt.plot(tiempos, setpoints, color="red")
        plt.plot(tiempos, posiciones, ".-")
        plt.plot(tiempos, controladores, ".-")
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
            "controlador": controladores,
            "Kp": [Kp1] * len(tiempos)/2 + [Kp2] * len(tiempos)/2,
            "Ki": [Ki1] * len(tiempos)/2 + [Ki2] * len(tiempos)/2,
            "Kd": [Kd1] * len(tiempos)/2 + [Kd2] * len(tiempos)/2,
            "ISE": [ISE] * len(tiempos)
        })

        os.makedirs(save_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Kp{Kp:.2f}_Ki{Ki:.2f}_Kd{Kd:.2f}_Set{setpoint}_ISE{ISE:.2f}_{timestamp}.csv"
        df.to_csv(os.path.join(save_folder, filename), index=False, header=True)

    return ISE


