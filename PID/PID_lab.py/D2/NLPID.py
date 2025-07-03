import numpy as np

y, t = input("y", "t") #medicion
sp = 300

r = sp
dt = t - t[-1]

e = r - y
de = (e - e[-1])/dt

n = 5 # antiwindup (tf)
integrador = sum(e[-n])


def NLPID(y, r, a=1, k0=1, k1=1, k2=1, k3=1):

    def kp(e,r):
        if r != 0:
            if abs(e/r) < 1:
                return a*k0 - k0*np.exp(1/((abs(e/r)**2) - 1)) 
            if abs(e/r) >= 1:
                return a*k0
        if r == 0:
            if abs(e) < 1:
                return a*k0 - k0*np.exp(1/((abs(e)**2) - 1))
            if abs(e) >= 1:
                return a*k0
            
    def ki(e,r):
        if r != 0:
            if abs(e/r) < 1:
                return k1*np.exp(1/((abs(e/r)**2) - 1)) 
            if abs(e/r) >= 1:
                return 0
        if r == 0:
            if abs(e) < 1:
                return k1*np.exp(1/((abs(e)**2) - k3**2))
            if abs(e) >= 1:
                return 0
    
    def kd(de,r):   
        if r != 0:
            if abs(de/r) < k3:
                return k2*np.exp(1/((abs(de/r)**2) - k3**2)) 
            if abs(de/r) >= k3:
                return 0
        if r == 0:
            if abs(de) < k3:
                return k2*np.exp(1/((abs(de)**2) - k3**2))
            if abs(de) >= k3:
                return 0

kp,ki,kd = NLPID(y,r)

controlador = e*kp + integrador*ki + de*kd # u(t)