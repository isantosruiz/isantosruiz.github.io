"""Transformadas y fracciones parciales con SymPy."""
import sympy as sp

t = sp.symbols("t", positive=True)
s = sp.symbols("s")

for f in (sp.exp(-2*t), t, sp.exp(-t)*sp.sin(2*t)):
    F, a, condicion = sp.laplace_transform(f, t, s)
    print("f(t) =", f)
    print("F(s) =", F, "; Re(s) >", a, "; condición:", condicion)

ejemplos = (
    2/(s*(s + 1)*(s + 2)),
    (s + 3)/(s + 2)**2,
    (s + 3)/(s**2 + 2*s + 5),
)
for F in ejemplos:
    f = sp.simplify(sp.inverse_laplace_transform(F, s, t))
    print("\nFracciones parciales:", sp.apart(F, s))
    print("Inversa para t > 0:", f)
    comprobacion = sp.laplace_transform(f, t, s, noconds=True)
    assert sp.simplify(comprobacion - F) == 0

# Un tiempo real permite representar explícitamente el encendido retardado.
tr = sp.symbols("tr", real=True)
retardo = sp.inverse_laplace_transform(sp.exp(-2*s)/s, s, tr)
print("\nEscalón retardado:", retardo)
