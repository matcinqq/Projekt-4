import numpy as np
import matplotlib.pyplot as plt
s = np.zeros(100)
e = np.zeros(100)
i = np.zeros(100)
r = np.zeros(100)

s[0] = 0.99
e[0] = 0.01
i[0] = 0
r[0] = 0

t = np.linspace(0, 20, 100)
h = t[1]-t[0]

beta = [0.5,2]
sigma = 1
gamma = 1 # zmiana 0.1 -> 1 (wyższy stopień ozdrowień)

R0 = [0,0]

for m in range(len(R0)):
    R0[m] = (beta[m]/gamma)*s[0]

def wyniki(beta):
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

    return s,e,i,r,

for m in range(len(beta)):
    s,e,i,r  = wyniki(beta[m])
    plt.plot(t,s, color = "green", label = "S")
    plt.plot(t,e, color = "red", label = "E")
    plt.plot(t,i, color = "black", label = "I")
    plt.plot(t,r, color = "blue", label = "R")
    plt.legend()
    plt.show()
print(R0)

"""
Analiza wyników: 
Nie jestem pewnien, czy dobrze zrozumiałem zadanie. Zmieniałem betę oraz gammę, w taki sposób,
by R0 było poniżej i powyżej 1. 

Przy R0 < 1 -> S (podatni na zachorowanie) początkowo lekko maleje, poczym pozostaje w zasadzie stałe
            -> E (wystawieni na działanie wirusa) powoli maleje, aż osiąga 0.
            -> I (zarażający) początkowo lekko rośnie, po czym też osiąga 0.
            -> R (przechorowani, zmarli) jednostajnie rośnie, osiąga granicę i staje się stałe na poziomie ~0.02
            => Wniosek: Jeśli parametr reprodukcji jest < 1 choroba nie ma jak rozwijać się w populacji.
               Liczba zachorowań stopniowo spada, aż choroba nie zaraża już nikogo. Trzeba też wziąć pod uwagę 
               zwiększony parametr wyzdrawiania (gamma).

Przy R0 < 1 -> S (podatni na zachorowanie) początkowo maleje lekko, następnie spadek przyśpiesza, potem znów zwalnia.        
            -> E (wystawieni na działanie wirusa) rośnie bardzo powoli, osiąga stosunkowo niski wierzchołek poczym ponownie spada 
            -> I (zarażający) podąża blisko za E. 
            -> R (przechorowani, zmarli) działa przeciwnie do S, rośnie: wolno -> szybko -> wolno.
            => Wniosek: Jeśli parametr reprodukcji jest > 1, beta jest stosunkowo małe, a gamma dość duże (gamma = 1),
               choroba może się rozwijać, do momentu, w którym poziom podatnych na zakarzenie spada poniżej ilości
               osób które przechorowały lub zmarły. Potem poziom chorych spada, jednak dość powoli i metodycznie.
               Można z tego wywnioskować, że choroba, gdy R0 > 1, może się rozwijać, jednak limitującymi warunkami jest
               szybki spadek poziomu osób które jeszcze nie przeszły choroby, a także stosunkowo duży parametr
               wyzdrowień. Fakt, że I bliso podąża za E może świadczyć o tym, że wysokie jest prawdopodobieństwo
               zachorowaniea po kontakcie, ale choroba nie może się rozwijać ponad miarę, przez wysoki parametr wyzdrowień.
            
"""