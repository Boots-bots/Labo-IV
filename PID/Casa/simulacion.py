import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime
import os

# Sistema simulado
class SistemaSimulado:
    def __init__(self, x0=0.0, v0=0.0, zeta=0.7, wn=1.5, Ku=1.0, dt=0.1):
        self.x = x0
        self.v = v0
        self.zeta = zeta
        self.wn = wn
        self.Ku = Ku
        self.dt = dt

    def avanzar(self, u):
        a = -2*self.zeta*self.wn*self.v - (self.wn**2)*self.x + self.Ku * u
        self.v += a * self.dt
        self.x += self.v * self.dt
        return self.x

# Suplantación de funciones físicas
simulador = None
def trackTemplate(vs=None, template=None, limites=None):
    return simulador.avanzar(trackTemplate.control_actual)
trackTemplate.control_actual = 0

def enviar_a_arduino(valor):
    trackTemplate.control_actual = int(valor.strip()[1:])

# Evaluación PID real sobre sistema simulado
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
    enviar_a_arduino(bytes(f'a153\n', 'utf-8'))
    time.sleep(2)

    t0 = time.time()

    while time.time() - t0 < duracion:
        tiempo_actual = time.time() - t0
        pos = trackTemplate()
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
        enviar_a_arduino(bytes(f'a{int(control_signal)}\n', 'utf-8'))

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
    enviar_a_arduino(bytes(f'a120\n', 'utf-8'))
    time.sleep(3)
    enviar_a_arduino(bytes(f'a0\n', 'utf-8'))

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

# % Inicialización del sistema simulado
simulador = SistemaSimulado(x0=0.0, v0=0.0, zeta=0.7, wn=1.2, Ku=0.8, dt=0.1)
trackTemplate.control_actual = 0

# Prueba del PID con simulación
K_test = [15, 1.5, 2.5]
ISE = evaluar_pid(K_test, duracion=20, setpoint=1.0, guardar_csv=False)
print(f"\n✅ Simulación finalizada con ISE = {ISE:.4f}")