import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import Bounds, LinearConstraint, minimize


def objetivo(x):
    return (x[0] - 3.0)**2 + 2.0*(x[1] - 2.0)**2


def gradiente(x):
    return np.array([2.0*(x[0] - 3.0), 4.0*(x[1] - 2.0)])


A = np.array([[1.0, 1.0]])
lb = np.array([0.0, 0.0])
ub = np.array([2.5, 3.0])
limite_total = LinearConstraint(A, -np.inf, 4.0)

resultado = minimize(
    objetivo,
    x0=np.array([1.0, 1.0]),
    jac=gradiente,
    method="SLSQP",
    bounds=Bounds(lb, ub),
    constraints=[limite_total],
    options={"ftol": 1e-12, "maxiter": 200},
)

if not resultado.success:
    raise RuntimeError(f"No se confirmó la convergencia: {resultado.message}")

x = resultado.x
tol = 1e-7
assert np.all(A @ x <= 4.0 + tol)
assert np.all(x >= lb - tol) and np.all(x <= ub + tol)
assert np.linalg.norm(x - np.array([7/3, 5/3])) < 1e-5
holguras = np.concatenate((4.0 - A @ x, ub - x, x - lb))

print(f"Corrientes [A]: {x[0]:.6f}, {x[1]:.6f}")
print(f"Costo de seguimiento: {objetivo(x):.6f}")
print("Holguras:", holguras)

X1, X2 = np.meshgrid(np.linspace(0, 3.5, 250), np.linspace(0, 3.5, 250))
F = (X1 - 3.0)**2 + 2.0*(X2 - 2.0)**2
vertices = np.array([[0, 0], [2.5, 0], [2.5, 1.5], [1, 3], [0, 3]])

fig, ax = plt.subplots(figsize=(7, 6), constrained_layout=True)
ax.fill(vertices[:, 0], vertices[:, 1], color="#d6eee8", alpha=0.7)
ax.contour(X1, X2, F, levels=[2/3, 1, 2, 4, 8, 12], linewidths=1)
ax.plot(3, 2, "kx", markersize=10, label="Referencia no factible")
ax.plot(*x, "ro", label="Solución óptima")
ax.set(xlabel=r"$x_1=I_1/I_0$", ylabel=r"$x_2=I_2/I_0$",
       xlim=(0, 3.5), ylim=(0, 3.5),
       title="Reparto de corriente con restricciones")
ax.set_aspect("equal")
ax.grid(alpha=0.25)
ax.legend()
plt.show()
