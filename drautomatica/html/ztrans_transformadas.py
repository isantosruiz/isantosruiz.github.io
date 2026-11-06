"""Transformada Z unilateral mediante sumas, fracciones parciales y series."""
import sympy as sp

k = sp.symbols("k", integer=True, nonnegative=True)
z, q = sp.symbols("z q")
a, b = sp.Rational(1, 2), sp.Rational(4, 5)

# summation devuelve también las condiciones de convergencia.
for x in (a**k, k*a**k):
    resultado = sp.summation(x*z**(-k), (k, 0, sp.oo))
    print("\nSecuencia:", x)
    print("Transformada y condiciones:", resultado)

# La inversa causal se reconoce descomponiendo X(z)/z.
X = z/((z-a)*(z-b))
x = (b**k-a**k)/(b-a)
print("\nFracciones parciales de X(z)/z:", sp.apart(X/z, z))
print("Inversa para k >= 0:", x)
assert sp.cancel(X - (z/(z-b)-z/(z-a))/(b-a)) == 0

# z^{-1}=q: el coeficiente de q^k es x[k].
serie = sp.series(X.subs(z, 1/q), q, 0, 9).removeO().expand()
for n in range(9):
    assert sp.simplify(serie.coeff(q, n)-x.subs(k, n)) == 0
print("Primeras muestras:", [x.subs(k, n) for n in range(6)])

# Un polo repetido genera un factor k, no un exponencial aislado.
X2 = z/(z-a)**2
x2 = k*a**(k-1)
serie2 = sp.series(X2.subs(z, 1/q), q, 0, 9).removeO().expand()
for n in range(9):
    assert sp.simplify(serie2.coeff(q, n)-x2.subs(k, n)) == 0
print("Inversa con polo repetido:", x2)

# Ecuación y[k+1] = a*y[k] + c*v[k], con y[0] = y0.
Y, V, y0, c = sp.symbols("Y V y0 c")
ecuacion = sp.Eq(z*(Y-y0), a*Y+c*V)
Ysol = sp.factor(sp.solve(ecuacion, Y)[0])
print("\nSolución transformada con condición inicial:", Ysol)
print("Valor inicial:", sp.limit(Ysol, z, sp.oo))
