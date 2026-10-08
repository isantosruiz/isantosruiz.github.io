"""Modelos RC y masa-resorte-amortiguador mediante Laplace."""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

t = sp.symbols("t", positive=True)
s, X = sp.symbols("s X")

# Circuito RC: R = 1000 ohm, C = 100 microfaradios.
R, C = sp.Integer(1000), sp.Rational(1, 10000)
V0, Vin = sp.Integer(1), sp.Integer(5)
Vc = (Vin/s + R*C*V0)/(R*C*s + 1)
vc = sp.simplify(sp.inverse_laplace_transform(Vc, s, t))
assert sp.simplify(R*C*sp.diff(vc, t) + vc - Vin) == 0
assert sp.limit(vc, t, 0, dir="+") == V0
print("Tensión del capacitor:", vc)

# Modelo mecánico, en unidades SI, con condiciones iniciales no nulas.
m, b, k, F0 = map(sp.Integer, (1, 2, 5, 5))
x0, v0 = sp.Rational(1, 5), sp.Integer(0)
ecuacion = sp.Eq(m*(s**2*X - s*x0 - v0)
                + b*(s*X - x0) + k*X, F0/s)
Xs = sp.factor(sp.solve(ecuacion, X)[0])
H = 1/(m*s**2 + b*s + k)
Xentrada = H*F0/s
Xinicial = H*((m*s + b)*x0 + m*v0)
x = sp.simplify(sp.inverse_laplace_transform(Xs, s, t))
xe = sp.simplify(sp.inverse_laplace_transform(Xentrada, s, t))
xi = sp.simplify(sp.inverse_laplace_transform(Xinicial, s, t))
assert sp.simplify(m*sp.diff(x,t,2) + b*sp.diff(x,t) + k*x - F0) == 0
assert sp.limit(x,t,0,dir="+") == x0
assert sp.limit(sp.diff(x,t),t,0,dir="+") == v0
assert sp.simplify(x - xe - xi) == 0
print("X(s) =", Xs)
print("x(t) =", x)
print("Polos:", sp.solve(m*s**2 + b*s + k, s))
print("Posición final:", sp.limit(s*Xs, s, 0))

tt = np.linspace(0, 8, 1601)
evaluar = lambda expresion, tiempo: sp.lambdify(t, expresion, "numpy")(tiempo)
fig, ax = plt.subplots(layout="constrained")
ax.plot(tt, evaluar(x,tt), label="Respuesta total")
ax.plot(tt, evaluar(xe,tt), "--", label="Debida a la fuerza")
ax.plot(tt, evaluar(xi,tt), ":", label="Debida al estado inicial")
ax.set(xlabel="Tiempo (s)", ylabel="Posición (m)")
ax.grid(alpha=0.25)
ax.legend()

# Segundo experimento: pulso de 5 N durante 2 s, desde el reposo.
T = 2.0
xp = evaluar(xe,tt).copy()
activos = tt >= T
xp[activos] -= evaluar(xe,tt[activos] - T)
fig2, (a1, a2) = plt.subplots(2, 1, sharex=True, layout="constrained")
a1.step(tt, float(F0)*(tt < T), where="post")
a1.set(ylabel="Fuerza (N)")
a2.plot(tt, xp)
a2.set(xlabel="Tiempo (s)", ylabel="Posición (m)")
for eje in (a1, a2):
    eje.grid(alpha=0.25)
plt.show()
