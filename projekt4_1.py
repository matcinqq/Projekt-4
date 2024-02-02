import numpy as np
import matplotlib.pyplot as plt
s = np.zeros(100)
e = np.zeros(100)
i = np.zeros(100)
r = np.zeros(100)

t = np.linspace(0, 10, 100)
h = t[1]-t[0]

beta = 1
sigma = 1
gamma = 0.1

s[0] = 0.99
e[0] = 0.01
i[0] = 0
r[0] = 0

def ds(s, i):
    ds = -beta * i * s
    return ds

def de(s, i, e):
    de = beta * i * s - sigma * e
    return de

def di(e, i):
    di = sigma * e - gamma * i
    return di

def dr(i):
    dr = gamma * i
    return dr


for v in range(1, len(t)):
    k1s = h * ds(s[v - 1], i[v - 1])
    k1e = h * de(s[v - 1], i[v - 1], e[v - 1])
    k1i = h * di(e[v - 1], i[v - 1])
    k1r = h * dr(i[v - 1])

    k2s = h * ds(s[v - 1] + 0.5 * k1s, i[v - 1] + 0.5 * k1i)
    k2e = h * de(s[v - 1] + 0.5 * k1s, i[v - 1] + 0.5 * k1i, e[v - 1] + 0.5 * k1e)
    k2i = h * di(e[v - 1] + 0.5 * k1e, i[v - 1] + 0.5 * k1i)
    k2r = h * dr(i[v - 1] + 0.5 * k1i)

    k3s = h * ds(s[v - 1] + 0.5 * k2s, i[v - 1] + 0.5 * k2i)
    k3e = h * de(s[v - 1] + 0.5 * k2s, i[v - 1] + 0.5 * k2i, e[v - 1] + 0.5 * k2e)
    k3i = h * di(e[v - 1] + 0.5 * k2e, i[v - 1] + 0.5 * k2i)
    k3r = h * dr(i[v - 1] + 0.5 * k2i)

    k4s = h * ds(s[v - 1] + k3s, i[v - 1] + k3i)
    k4e = h * de(s[v - 1] + k3s, i[v - 1] + k3i, e[v - 1] + k3e)
    k4i = h * di(e[v - 1] + k3e, i[v - 1] + k3i)
    k4r = h * dr(i[v - 1] + k3i)

    s[v] = s[v - 1] + (k1s + 2 * k2s + 2 * k3s + k4s) / 6
    e[v] = e[v - 1] + (k1e + 2 * k2e + 2 * k3e + k4e) / 6
    i[v] = i[v - 1] + (k1i + 2 * k2i + 2 * k3i + k4i) / 6
    r[v] = r[v - 1] + (k1r + 2 * k2r + 2 * k3r + k4r) / 6

plt.plot(t,s, color = "green", label = "S")
plt.plot(t,e, color = "red", label = "E")
plt.plot(t,i, color = "black", label = "I")
plt.plot(t,r, color = "blue", label = "R")
plt.legend()
plt.show()
