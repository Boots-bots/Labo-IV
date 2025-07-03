# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 10:23:06 2025

@author: Publico
"""

# imports

import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt 
import cv2 #esto conecta la camara al programa
import serial as ser
import time
from scipy.signal import sawtooth
import serial.tools.list_ports


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
arduino = ser.Serial(port='COM13', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.05, xonxoff=0, rtscts=0)
time.sleep(2)

#%% Guardado imagen del vaso, en escala de grises
im = vs.read()[1]
im = np.mean(im, axis=2)
imsave('completa.png', im, cmap='gray')
temp = cv2.imread('completa.png')
cv2.imshow("",temp)

# Guardado imagen recortada (tubo/template), en escala de grises
im = vs.read()[1]
limites_vasito=[2,92, 200, 270]#[480,590, 200, 277]#[54,145, 190, 260]
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
arduino.write(bytes(f'a200\n', 'utf-8'))
#time.sleep(15)
arduino.write(bytes(f'a155\n', 'utf-8')) # 152 ± 5 estabilidad
#%% prueba camara

duracion = 100
valor = 0

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
    if pos < 10:
        arduino.write(bytes(f'a200\n', 'utf-8'))

print("Finich")

#%% plot
plt.figure()
plt.plot(tiempo, posicion,".-")
plt.xlabel("Tiempo [s]")
plt.ylabel("Posicion [pix]")

#%% Inicialización variables para loop
cero = 153

def set_ventilador(val):
    valor = val + cero
    if valor < 0:
        valor=0
    elif valor > 255:
        valor = 255

    arduino.write(bytes(f'a{valor}\n', 'utf-8'))


#%%   Medicion con los Ks
duracion = 60
setpoint = 300
integra = True

kc = 0.25

Kp = kc*10

average_period = 8
ftg = 0.03       #POR FOTOGRAMA 

Ki= 25*ftg*kc / average_period
Kd = 7*kc

#%% Medicion Optimo

# Apagado ventiladores
#valor = 0
#arduino.write(bytes(f'a{valor}\n', 'utf-8'))
#time.sleep(4)

integrador = 0
error_anterior = 0
errores_recientes = []  # Lista para almacenar los últimos 5 errores
derivativo = 0

tiempo = []
posicion = []
integradores = []
proporcionales = []
derivativos = []

t0 = time.time()

i= 0
while time.time() - t0 < duracion:
    tiempo.append(time.time() - t0)
    pos = trackTemplate(vs, template, limites_tubo)
    if pos is None:
        print("No se pudo detectar la posición")
        continue
    
    posicion.append(pos)

    # Calcular el término proporcional
    error = setpoint - pos
    errores_recientes.append(error)
    proporcional = Kp*error
    
    # Calcular dt (tiempo entre iteraciones)
    if len(tiempo) > 1:
       dt = tiempo[-1] - tiempo[-2]  # Tiempo actual - Tiempo anterior
    else:
        dt = 0  # En la primera iteración, no hay dt válido

    # Calcular el término integrador
    if integra == True:
        errores_desde = i
        integrador = Ki * sum(errores_recientes[(errores_desde-4):])  # Solo suma los últimos 5 errores
        # Termino integrador necesita una cota p/ej 255- (-255)
    
    # Calcular el término derivativo
        
    if (len(posicion) >= 3):
        derivativo = Kd*(errores_recientes[-1] - errores_recientes[-3]) / (dt*2)
    else:
        # Manejar el caso en que no haya suficientes datos en 'posicion'
        derivativo = 0
    
    #elif abs(derivativo)>0:
    #    print(tiempo[-ultimos:], posicion[-ultimos:])
    #    derivativo = Kd*promediarUltimos(tiempo[-ultimos:], posicion[-ultimos:])


    proporcionales.append(proporcional)
    integradores.append(integrador)
    derivativos.append(derivativo)
    
    
    control_signal = proporcional + integrador + derivativo
    
    # Aplicar el control proporcional
    
    if control_signal < 0:
        control_signal=0
    elif control_signal > 255:
        control_signal = 255  # Limitar el valor dentro del rango permitido (0-255)
    arduino.write(bytes(f'a{control_signal}\n', 'utf-8'))
    
    #set_ventilador(control_signal)
    
    i=i+1

print("Finish")
arduino.write(bytes(f'a{120}\n', 'utf-8'))
time.sleep(5)
arduino.write(bytes(f'a{0}\n', 'utf-8'))
#%%
plt.figure()
plt.title("Posición")
plt.axhline(setpoint, linestyle = "--")
plt.plot(tiempo, posicion,".-")
plt.xlabel("Tiempo [s]")
plt.ylabel("Posicion [pix]")
plt.grid()

plt.figure()
plt.title("Término Proporcional")
plt.plot(tiempo, proporcionales,".-")
plt.xlabel("Tiempo [s]")
plt.ylabel("Posicion [pix]")
plt.grid()

plt.figure()
plt.title("Término Integrativo")
plt.plot(tiempo, integradores,".-")
plt.xlabel("Tiempo [s]")
plt.ylabel("Posicion [pix]")
plt.grid()

plt.figure()
plt.title("Término Derivativo")
plt.plot(tiempo, derivativos,".-")
plt.xlabel("Tiempo [s]")
plt.ylabel("Posicion [pix]")
plt.grid()

#%%
