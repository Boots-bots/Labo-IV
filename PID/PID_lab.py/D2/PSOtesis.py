import numpy as np
import time

# Simulacion ficticia que imita Simulink
# Reemplazar esto con llamada real a simulador

def simulate_pid(k0, k1, a, k2):
    # Devuelve una tupla: (error_array, tiempo_array, settling_time)
    # Simulacion simplificada, la funcion ISE dependera del error
    t = np.linspace(0, 10, 1000)
    error = np.exp(-a * t) * np.sin(k0 * t)  # ejemplo de error
    settling_time = 5  # valor fijo arbitrario
    return error, t, settling_time

# Funcion de costo: ISE

def ise(error, t, settling_time):
    mask = t <= settling_time
    return np.trapz(error[mask]**2, t[mask])

# Parametros de la simulacion
nvars = 4  # k0, k1, a, k2
PN = 30
MaxIteration = 90
k0max = 2
k1max = 2
k2max = 2
amax = 2
amin = 0.5

# Inicializacion
np.random.seed(0)
x = 2 * np.abs(np.random.rand(PN, nvars))
v = np.zeros((PN, nvars))
pbest = x.copy()
pbest_val = np.full(PN, np.inf)
gbest = np.zeros(nvars)
gbest_val = np.inf

start_time = time.time()

for i in range(MaxIteration):
    for j in range(PN):
        k0, k1, a, k2 = x[j]

        # Saturacion de parametros
        k0 = min(abs(k0), k0max)
        k1 = min(abs(k1), k1max)
        k2 = min(abs(k2), k2max)
        a = np.clip(abs(a), amin, amax)

        # Simulacion
        try:
            error, t_arr, st = simulate_pid(k0, k1, a, k2)
        except:
            continue

        obj = ise(error, t_arr, st)

        # Actualizar mejor personal
        if obj < pbest_val[j]:
            pbest[j] = x[j].copy()
            pbest_val[j] = obj

        # Actualizar mejor global
        if obj < gbest_val:
            gbest = x[j].copy()
            gbest_val = obj

    # Actualizacion de velocidad y posicion (solo Gbest, sin Pbest ni inercia)
    c1 = 1.3
    for j in range(PN):
        for k in range(nvars):
            r1 = np.random.rand()
            phi1 = c1 * r1
            v[j, k] = abs(v[j, k] + phi1 * (gbest[k] - x[j, k]))
            x[j, k] = abs(x[j, k] + v[j, k])

# Resultado final
k0, k1, a, k2 = gbest
print("Mejores parametros:")
print(f"k0 = {k0:.4f}, k1 = {k1:.4f}, a = {a:.4f}, k2 = {k2:.4f}")
print(f"Costo minimo (ISE): {gbest_val:.4f}")
print(f"Tiempo de ejecucion: {time.time() - start_time:.2f} segundos")
