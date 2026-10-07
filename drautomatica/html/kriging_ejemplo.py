"""Kriging ordinario con tres sensores y semivariograma lineal.

Presiones en psi, coordenadas en unidades de longitud (u.l.) y pendiente
c = 1 psi^2/u.l. El modelo es didáctico; no se ajusta a mediciones reales.
Requiere sympy, numpy y matplotlib. Los PNG se guardan junto al script.
"""

import sympy as sp

P1 = sp.Point(0, 0)
P2 = sp.Point(4, 0)
P3 = sp.Point(0, 3)
P0 = sp.Point(2, 2)
z = sp.Matrix([30, 28, 35])
c = sp.Integer(1)  # Valor numérico en psi^2/u.l.


def gamma(punto_a, punto_b):
    return c * punto_a.distance(punto_b)


# Matriz ampliada de semivarianzas, no de covarianzas.
A = sp.Matrix([
    [gamma(P1, P1), gamma(P1, P2), gamma(P1, P3), 1],
    [gamma(P2, P1), gamma(P2, P2), gamma(P2, P3), 1],
    [gamma(P3, P1), gamma(P3, P2), gamma(P3, P3), 1],
    [1,             1,             1,             0],
])
b = sp.Matrix([
    gamma(P1, P0), gamma(P2, P0), gamma(P3, P0), 1
])

detA = A.det()
if detA == 0:
    raise ValueError("Matriz singular. No existe solución única.")

u = A.LUsolve(b).applyfunc(sp.simplify)
w = u[0:3, 0]
multiplicador = u[3]
z0 = sp.simplify(w.dot(z))
varianza_kriging = sp.simplify(u.dot(b))
error_estandar = sp.sqrt(varianza_kriging)

print("=" * 48)
print("REPORTE DE INTERPOLACIÓN GEOESTADÍSTICA")
print("=" * 48)
print(f"Determinante de A: {detA}")
for i, peso in enumerate(w, start=1):
    print(f"w{i}: {float(peso):.6f}")
print(f"Suma de comprobación: {float(sum(w)):.6f}")
print(f"Multiplicador: {float(multiplicador):.6f} psi²")
print(f"Presión estimada en P0: {float(z0):.6f} psi")
print(f"Incertidumbre (varianza): {float(varianza_kriging):.6f} psi²")
print(f"Error estándar: {float(error_estandar):.6f} psi")
print("=" * 48)

# Múltiples puntos objetivo, con el mismo modelo y los mismos sensores.
import numpy as np

puntos = np.array([list(P1), list(P2), list(P3)], dtype=float)
valores = np.array(z, dtype=float).ravel()
A_num = np.array(A, dtype=float)
X, Y = np.meshgrid(np.linspace(-1, 5, 241), np.linspace(-1, 4, 201))
objetivos = np.column_stack((X.ravel(), Y.ravel()))
distancias = np.linalg.norm(
    puntos[:, None, :] - objetivos[None, :, :], axis=2
)
B = np.vstack((float(c) * distancias, np.ones(objetivos.shape[0])))
U = np.linalg.solve(A_num, B)
presiones = (valores @ U[:3, :]).reshape(X.shape)
varianzas = np.sum(U * B, axis=0).reshape(X.shape)

# Solo se corrigen residuos negativos del orden del redondeo numérico.
tolerancia = 1e-10 * max(1.0, np.max(np.abs(B)))
if np.min(varianzas) < -tolerancia:
    raise ValueError("Varianza negativa: revise el modelo y el sistema.")
desviaciones = np.sqrt(np.maximum(varianzas, 0.0))

# Figuras con la misma escala geométrica y variables en tipografía matemática.
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "mathtext.fontset": "stix",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.facecolor": "white",
})
salida = Path(__file__).resolve().parent

mapas = [
    (presiones, "viridis", "Presión estimada (psi)",
     "kriging-presion.png", float(presiones.min()), float(presiones.max())),
    (desviaciones, "YlGnBu", "Error estándar (psi)",
     "kriging-incertidumbre.png", 0, float(desviaciones.max())),
]

for campo, paleta, etiqueta, archivo, minimo, maximo in mapas:
    fig, ax = plt.subplots(figsize=(8.0, 5.5), layout="constrained")
    imagen = ax.pcolormesh(
        X, Y, campo, cmap=paleta, shading="auto", vmin=minimo, vmax=maximo
    )
    ax.plot([0, 4, 0, 0], [0, 0, 3, 0], "--", color="white", lw=1.5)
    ax.scatter(puntos[:, 0], puntos[:, 1], s=55, c="white",
               edgecolors="#202c32", linewidths=1.3, zorder=4, clip_on=False)
    ax.scatter([2], [2], s=75, marker="X", c="white",
               edgecolors="#202c32", linewidths=1.0, zorder=4)
    etiquetas = [
        ((0, 0), (12, 12), r"$P_1$ · 30 psi", "left", "bottom"),
        ((4, 0), (-12, 12), r"$P_2$ · 28 psi", "right", "bottom"),
        ((0, 3), (12, -12), r"$P_3$ · 35 psi", "left", "top"),
        ((2, 2), (12, 8), r"$P_0$", "left", "bottom"),
    ]
    for punto, desplazamiento, texto, horizontal, vertical in etiquetas:
        anotacion = ax.annotate(
            texto, punto, xytext=desplazamiento, textcoords="offset points",
            ha=horizontal, va=vertical, color="#17282c", fontsize=12.5
        )
        anotacion.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])
    ax.set(xlim=(-1, 5), ylim=(-1, 4), xlabel=r"$x$ (u.l.)", ylabel=r"$y$ (u.l.)")
    ax.set_aspect("equal")
    barra = fig.colorbar(imagen, ax=ax, shrink=0.86, pad=0.035)
    barra.set_label(etiqueta)
    barra.outline.set_visible(False)
    fig.savefig(salida / archivo, dpi=220)
    plt.close(fig)
