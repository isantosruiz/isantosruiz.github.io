"""Convolución, circuito RC y mecanismo muestreado con retención de orden cero."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from scipy.signal import lfilter


def crear_figuras():
    figuras = {}

    # Convolución causal: la salida tiene una cola aunque la entrada termine.
    k = np.arange(16)
    entrada = np.array([1., 1., 1.])
    h = 0.5**k
    salida = np.convolve(entrada, h)[:len(k)]
    salida_rec = lfilter([1.], [1., -0.5], np.pad(entrada, (0, 13)))
    assert np.allclose(salida, salida_rec, rtol=0, atol=1e-12)
    fig, axes = plt.subplots(3, 1, sharex=True, layout="constrained")
    for ax, valores, titulo in zip(axes, (np.pad(entrada, (0, 13)), h, salida),
                                   ("Entrada v[k]", "Respuesta al impulso h[k]",
                                    "Salida y[k] = (h * v)[k]")):
        ax.stem(k, valores, basefmt=" ")
        ax.set(ylabel="Amplitud", title=titulo)
        ax.grid(alpha=0.2)
    axes[-1].set_xlabel("Índice k")
    figuras["convolucion"] = fig

    # RC: R = 1 kohm, C = 100 microfaradios, Ts = 20 ms.
    R, C, Ts = 1000., 100e-6, 0.02
    a = np.exp(-Ts/(R*C))
    k = np.arange(31)
    t = k*Ts
    V0, Vin = 1., 5.
    vc = np.empty(len(k)); vc[0] = V0
    for n in range(len(k)-1):
        vc[n+1] = a*vc[n] + (1-a)*Vin
    inicial = V0*a**k
    forzada = Vin*(1-a**k)
    assert np.allclose(vc, inicial+forzada, rtol=0, atol=1e-12)
    assert np.allclose(vc, Vin+(V0-Vin)*a**k, rtol=0, atol=1e-12)
    assert np.allclose(np.diff(vc), (1-a)*(Vin-vc[:-1]), rtol=0, atol=1e-12)
    fig, ax = plt.subplots(layout="constrained")
    tt = np.linspace(0, t[-1], 601)
    ax.plot(tt, Vin+(V0-Vin)*np.exp(-tt/(R*C)), color="0.55",
            lw=1.3, label="Evolución continua")
    ax.plot(t, forzada, "--", label="Debida a la entrada")
    ax.plot(t, inicial, ":", label="Debida al estado inicial")
    ax.plot(t, vc, "o", ms=4, label="Muestras del modelo discreto")
    ax.set(xlabel="Tiempo (s)", ylabel="Tensión del capacitor (V)")
    ax.grid(alpha=0.2); ax.legend()
    figuras["rc"] = fig

    # Mecanismo: m = 1 kg, b = 2 N s/m, K = 5 N/m, Ts = 0.2 s.
    m, b, K, Ts = 1., 2., 5., 0.2
    A = np.array([[0., 1.], [-K/m, -b/m]])
    B = np.array([[0.], [1/m]])
    # Exponencial de la matriz aumentada: no requiere invertir A.
    E = expm(np.block([[A, B], [np.zeros((1, 3))]])*Ts)
    Ad, Bd = E[:2, :2], E[:2, 2]
    polos = np.linalg.eigvals(Ad)
    r, theta = np.exp(-Ts), 2*Ts
    den = np.array([1., -2*r*np.cos(theta), r*r])
    beta1 = (1-r*(np.cos(theta)+0.5*np.sin(theta)))/K
    beta2 = (1+den[1]+den[2])/K-beta1
    print("Ad =\n", Ad, "\nBd =", Bd)
    print("Polos:", polos)
    print("G(z): numerador en z^-1 =", [0., beta1, beta2])
    print("G(z): denominador en z^-1 =", den)
    assert np.all(np.abs(polos) < 1)

    k = np.arange(41); t = k*Ts
    F0, N = 5., 10
    fuerzas = (np.full(len(k), F0), F0*(k < N))
    titulos = ("Fuerza constante de 5 N", "Pulso de 5 N durante 2 s")
    fig, axes = plt.subplots(2, 1, sharex=True, layout="constrained")
    for ax, fuerza, titulo in zip(axes, fuerzas, titulos):
        estado = np.zeros((len(k), 2))
        for n in range(len(k)-1):
            estado[n+1] = Ad@estado[n] + Bd*fuerza[n]
        y = estado[:, 0]
        y_filtro = lfilter([0., beta1, beta2], den, fuerza)
        assert np.allclose(y, y_filtro, rtol=0, atol=1e-12)
        continua = F0/K*(1-np.exp(-t)*(np.cos(2*t)+0.5*np.sin(2*t)))
        if fuerza[-1] == 0:
            activos = k >= N
            tr = t[activos]-N*Ts
            continua[activos] -= F0/K*(1-np.exp(-tr)*(np.cos(2*tr)+0.5*np.sin(2*tr)))
        assert np.allclose(y, continua, rtol=0, atol=1e-12)
        ax.plot(t, y, "o", ms=4, label="Modelo discreto exacto")
        tt = np.linspace(0, t[-1], 1601)
        yc = F0/K*(1-np.exp(-tt)*(np.cos(2*tt)+0.5*np.sin(2*tt)))
        if fuerza[-1] == 0:
            mask = tt >= N*Ts; tr = tt[mask]-N*Ts
            yc[mask] -= F0/K*(1-np.exp(-tr)*(np.cos(2*tr)+0.5*np.sin(2*tr)))
        ax.plot(tt, yc, color="0.55", lw=1.2, label="Evolución continua")
        ax.set(ylabel="Posición (m)", title=titulo)
        ax.grid(alpha=0.2); ax.legend()
    axes[-1].set_xlabel("Tiempo (s)")
    figuras["mecanismo"] = fig
    return figuras


if __name__ == "__main__":
    crear_figuras()
    plt.show()
